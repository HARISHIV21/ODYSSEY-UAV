from mavsdk.telemetry import Battery


class BatteryMonitor:

    def __init__(self, drone):

        self.drone = drone
        self.last_battery = None

    async def get_battery(self):

        async for battery in self.drone.telemetry.battery():

            self.last_battery = battery
            return battery

    async def print_status(self):

        battery = await self.get_battery()

        if battery is None:

            print("[BATTERY] No Data")
            return

        print("\n========== BATTERY ==========")
        print(f"Remaining : {battery.remaining_percent:.1f}%")
        print(f"Voltage   : {battery.voltage_v:.2f} V")
        print("=============================\n")

    async def is_low(self, threshold=20):

        battery = await self.get_battery()

        if battery is None:
            return False

        return battery.remaining_percent * 100 <= threshold

    async def wait_until_safe(self, minimum=30):

        while True:

            battery = await self.get_battery()

            if battery is None:
                continue

            if battery.remaining_percent * 100 >= minimum:
                return
