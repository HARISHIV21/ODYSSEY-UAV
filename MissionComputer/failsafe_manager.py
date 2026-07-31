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

            self.log_warning(
                f"Battery check unavailable: {e}"
            )

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

            self.log_warning(
                f"Health check unavailable: {e}"
            )

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

        # Prevent accidental duplicate failsafe execution
        if self.active:

            print(
                "[FAILSAFE] Failsafe already active"
            )

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

        print("\n==============================")
        print("ODYSSEY FAILSAFE")
        print("==============================")

        print(
            f"[FAILSAFE] Reason: {self.reason}"
        )

        # -------------------------------------------------
        # STOP OFFBOARD
        # -------------------------------------------------

        try:

            print(
                "[FAILSAFE] Stopping Offboard..."
            )

            await self.fm.offboard.stop()

            print(
                "[FAILSAFE] Offboard stopped"
            )

        except Exception as e:

            print(
                f"[FAILSAFE] Offboard stop warning: {e}"
            )

        # -------------------------------------------------
        # LAND
        # -------------------------------------------------

        landing_successful = False

        try:

            print(
                "[FAILSAFE] Commanding landing..."
            )

            await self.fm.land()

            landing_successful = True

            print(
                "[FAILSAFE] Landing command accepted"
            )

        except Exception as e:

            self.log_error(
                f"Landing command failed: {e}"
            )

        # -------------------------------------------------
        # DISARM
        # -------------------------------------------------

        try:

            print(
                "[FAILSAFE] Attempting disarm..."
            )

            await self.fm.disarm()

            print(
                "[FAILSAFE] Disarm command completed"
            )

        except Exception as e:

            print(
                f"[FAILSAFE] Disarm warning: {e}"
            )

        # -------------------------------------------------
        # FINAL STATUS
        # -------------------------------------------------

        print("\n==============================")

        if landing_successful:

            print(
                "[FAILSAFE] VEHICLE SAFE"
            )

        else:

            print(
                "[FAILSAFE] LANDING STATUS UNKNOWN"
            )

        print(
            f"[FAILSAFE] Reason: {self.reason}"
        )

        print("==============================")
