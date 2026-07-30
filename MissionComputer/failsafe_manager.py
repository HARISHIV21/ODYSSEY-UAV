from MissionComputer.state_machine import MissionState


class FailsafeManager:

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

    async def check(self):

        # Battery Check
        if await self.battery.is_low(20):

            if self.logger:
                self.logger.log_warning(
                    "Battery Low - Activating Failsafe"
                )

            return MissionState.FAILSAFE

        # Health Check
        if not await self.health.check():

            if self.logger:
                self.logger.log_warning(
                    "Vehicle Health Failed"
                )

            return MissionState.FAILSAFE

        return MissionState.MISSION

    async def execute(self):

        if self.logger:
            self.logger.log_error(
                "FAILSAFE ACTIVATED"
            )

        print("\n==============================")
        print("FAILSAFE")
        print("==============================")

        # Stop Offboard safely
        try:
            await self.fm.offboard.stop()
        except Exception:
            pass

        # Attempt Landing
        try:
            print("[FAILSAFE] Landing...")

            await self.fm.land()

        except Exception as e:

            print(f"[FAILSAFE] Landing Failed : {e}")

        # Disarm
        try:
            await self.fm.disarm()
        except Exception:
            pass

        print("[FAILSAFE] Vehicle Safe")
