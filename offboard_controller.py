import asyncio
from mavsdk.offboard import PositionNedYaw, OffboardError


class OffboardController:
    def __init__(self, drone):
        self.drone = drone

    async def start(self, takeoff_altitude=None):
        """
        Start PX4 Offboard mode.

        Parameters
        ----------
        takeoff_altitude : float | None
            Accepted for compatibility with app.py.
            The current implementation does not require it because
            PX4 is already airborne after takeoff.
        """

        print("\n[OFFBOARD] Initializing...")

        # PX4 requires one setpoint before Offboard can be started.
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

        except OffboardError as error:
            print(f"[OFFBOARD] Failed to start: {error}")
            raise

    async def goto(
        self,
        north,
        east,
        down,
        yaw=0.0,
        hold_time=5,
    ):

        print(
            f"\n[OFFBOARD] Waypoint -> "
            f"N:{north:.2f} "
            f"E:{east:.2f} "
            f"D:{down:.2f} "
            f"Yaw:{yaw:.2f}"
        )

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
        print("\n[OFFBOARD] Stopping...")

        try:
            await self.drone.offboard.stop()
            print("[OFFBOARD] Stopped")

        except OffboardError:
            print("[OFFBOARD] Already stopped")
