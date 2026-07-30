import asyncio
from mavsdk.offboard import PositionNedYaw, OffboardError


class OffboardController:

    def __init__(self, drone):
        self.drone = drone

    async def start(self, takeoff_altitude=None):

        print("[OFFBOARD] Initializing...")

        await self.drone.offboard.set_position_ned(
            PositionNedYaw(
                north_m=0.0,
                east_m=0.0,
                down_m=0.0,
                yaw_deg=0.0,
            )
        )

        try:
            await self.drone.offboard.start()
            print("[OFFBOARD] Started Successfully")

        except OffboardError as e:
            print(f"[OFFBOARD] Failed: {e}")
            raise

    async def goto(self, north, east, down, yaw=0.0, hold_time=5):

        print(f"[OFFBOARD] Moving -> N:{north} E:{east} D:{down}")

        await self.drone.offboard.set_position_ned(
            PositionNedYaw(
                north_m=north,
                east_m=east,
                down_m=down,
                yaw_deg=yaw,
            )
        )

        await asyncio.sleep(hold_time)

    async def stop(self):

        try:
            await self.drone.offboard.stop()
            print("[OFFBOARD] Stopped")

        except OffboardError:
            pass
