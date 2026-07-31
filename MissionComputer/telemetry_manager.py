import asyncio


class TelemetryManager:

    def __init__(self, drone):

        self.drone = drone

        self.north = 0.0
        self.east = 0.0
        self.down = 0.0

        self.battery = 0.0
        self.flight_mode = "UNKNOWN"

        self.position_received = False
        self.battery_received = False
        self.mode_received = False

    async def get_position_once(self):

        async for data in self.drone.telemetry.position_velocity_ned():

            self.north = data.position.north_m
            self.east = data.position.east_m
            self.down = data.position.down_m

            self.position_received = True

            return

    async def get_battery_once(self):

        async for battery in self.drone.telemetry.battery():

            # MAVSDK Python reports remaining_percent
            # as a percentage value.
            self.battery = battery.remaining_percent

            self.battery_received = True

            return

    async def get_flight_mode_once(self):

        async for mode in self.drone.telemetry.flight_mode():

            self.flight_mode = str(mode)

            self.mode_received = True

            return

    async def update(self):

        results = await asyncio.gather(
            self.get_position_once(),
            self.get_battery_once(),
            self.get_flight_mode_once(),
            return_exceptions=True
        )

        errors = []

        for result in results:

            if isinstance(result, Exception):
                errors.append(result)

        if errors:
            raise errors[0]

    def ready(self):

        return (
            self.position_received
            and self.battery_received
        )

    def get_snapshot(self):

        return {
            "north": self.north,
            "east": self.east,
            "down": self.down,
            "battery": self.battery,
            "flight_mode": self.flight_mode
        }
