from MissionComputer.state_machine import MissionState


class FailsafeManager:

    LOW_BATTERY_THRESHOLD = 20

    def __init__(
        self,
        flight_manager,
        battery_monitor,
        health_monitor,
        logger=None,
    ):

        self.fm = flight_manager
        self.battery = battery_monitor
        self.health = health_monitor
        self.logger = logger

        self.active = False
        self.reason = None

    # -------------------------------------------------
    # LOGGING
    # -------------------------------------------------

    def log_warning(self, message):

        print(f"[FAILSAFE] WARNING: {message}")

        if self.logger:

            try:
                self.logger.log_warning(message)
            except Exception:
                pass

    def log_error(self, message):

        print(f"[FAILSAFE] ERROR: {message}")

        if self.logger:

            try:
                self.logger.log_error(message)
            except Exception:
                pass

    # -------------------------------------------------
    # BATTERY CHECK
    # -------------------------------------------------

    async def check_battery(self):

        try:

            if await self.battery.is_low(
                self.LOW_BATTERY_THRESHOLD
            ):

                self.reason = "LOW BATTERY"

                self.log_warning(
                    f"Battery below "
                    f"{self.LOW_BATTERY_THRESHOLD}%"
                )

                return False

        except Exception as e:

            self.reason = "BATTERY TELEMETRY FAILURE"

            self.log_warning(
                f"Battery check unavailable: {e}"
            )

            return False

        return True

    # -------------------------------------------------
    # VEHICLE HEALTH CHECK
    # -------------------------------------------------

    async def check_health(self):

        try:

            healthy = await self.health.check()

            if not healthy:

                self.reason = "VEHICLE HEALTH FAILURE"

                self.log_warning(
                    "Vehicle health check failed"
                )

                return False

        except Exception as e:

            self.reason = "VEHICLE HEALTH TELEMETRY FAILURE"

            self.log_warning(
                f"Health check unavailable: {e}"
            )

            return False

        return True

    # -------------------------------------------------
    # COMPLETE FAILSAFE CHECK
    # -------------------------------------------------

    async def check(self):

        battery_ok = await self.check_battery()

        if not battery_ok:

            return MissionState.FAILSAFE

        health_ok = await self.check_health()

        if not health_ok:

            return MissionState.FAILSAFE

        return MissionState.MISSION

    # -------------------------------------------------
    # MANUAL FAILSAFE TRIGGER
    # -------------------------------------------------

    async def trigger(self, reason):

        self.reason = reason

        self.log_error(
            f"Failsafe requested: {reason}"
        )

        await self.execute()

    # -------------------------------------------------
    # FAILSAFE EXECUTION
    # -------------------------------------------------

    async def execute(self):

        if self.active:
            print("[FAILSAFE] Failsafe already active")
            return

        self.active = True

        if self.reason is None:
            self.reason = "MISSION EXECUTION FAILURE"

        if self.logger:
            try:
                self.logger.log_error(
                    f"FAILSAFE ACTIVATED - {self.reason}"
                )
            except Exception:
                pass

        print("\\n==============================")
        print("ODYSSEY FAILSAFE")
        print("==============================")
        print(f"[FAILSAFE] Reason: {self.reason}")

        try:
            print("[FAILSAFE] Stopping Offboard...")
            await self.fm.offboard.stop()
            print("[FAILSAFE] Offboard stopped")
        except Exception as e:
            print(f"[FAILSAFE] Offboard stop warning: {e}")

        landing_confirmed = False
        disarm_confirmed = False

        try:
            print("[FAILSAFE] Commanding landing...")
            await self.fm.land()
            print("[FAILSAFE] Landing command accepted")

            await self.fm.wait_until_landed(timeout=60.0)
            landing_confirmed = True
            print("[FAILSAFE] Landing confirmed")

        except Exception as e:
            self.log_error(
                f"Landing could not be confirmed: {e}"
            )

        if landing_confirmed:
            try:
                await self.fm.wait_until_disarmed(timeout=3.0)
                disarm_confirmed = True

            except TimeoutError:
                try:
                    print("[FAILSAFE] Requesting disarm...")
                    await self.fm.disarm()
                    await self.fm.wait_until_disarmed(timeout=15.0)
                    disarm_confirmed = True
                except Exception as e:
                    self.log_error(
                        f"Disarm could not be confirmed: {e}"
                    )

            except Exception as e:
                self.log_error(
                    f"Disarm telemetry unavailable: {e}"
                )

        print("\\n==============================")

        if landing_confirmed and disarm_confirmed:
            print("[FAILSAFE] VEHICLE SAFE")
        elif not landing_confirmed:
            print("[FAILSAFE] LANDING STATUS UNKNOWN")
        else:
            print("[FAILSAFE] LANDING CONFIRMED - DISARM UNCONFIRMED")

        print(f"[FAILSAFE] Reason: {self.reason}")
        print("==============================")
