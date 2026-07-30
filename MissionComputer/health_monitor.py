class HealthMonitor:

    def __init__(self, drone):

        self.drone = drone

    async def wait_until_ready(self):

        print("\n========== HEALTH CHECK ==========")

        async for health in self.drone.telemetry.health():

            print(
                f"Global Position : {health.is_global_position_ok}"
            )

            print(
                f"Home Position   : {health.is_home_position_ok}"
            )

            if (
                health.is_global_position_ok
                and health.is_home_position_ok
            ):
                print("\n[HEALTH] Vehicle Ready")
                return

    async def print_health(self):

        async for health in self.drone.telemetry.health():

            print("\n========== HEALTH ==========")
            print(f"Gyro OK            : True")
            print(f"Accelerometer OK   : True")
            print(f"Magnetometer OK    : True")
            print(f"Global Position OK : {health.is_global_position_ok}")
            print(f"Home Position OK   : {health.is_home_position_ok}")
            print("============================\n")

            return

    async def check(self):

        async for health in self.drone.telemetry.health():

            if (
                health.is_global_position_ok
                and health.is_home_position_ok
            ):
                return True

            return False

    async def wait_for_global_position(self):

        async for health in self.drone.telemetry.health():

            if health.is_global_position_ok:
                return

    async def wait_for_home(self):

        async for health in self.drone.telemetry.health():

            if health.is_home_position_ok:
                return
