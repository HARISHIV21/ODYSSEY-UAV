import asyncio


class TelemetryManager:

    def __init__(self, drone):
        self.drone = drone

    async def monitor(self):

        async for position in self.drone.telemetry.position():

            print("\n-----------------------------")

            print(
                f"LATITUDE  : {position.latitude_deg:.6f}"
            )

            print(
                f"LONGITUDE : {position.longitude_deg:.6f}"
            )

            print(
                f"ALTITUDE  : {position.relative_altitude_m:.2f} m"
            )

            print("-----------------------------")

            await asyncio.sleep(1)
