from mavsdk import System

from MissionComputer.offboard_controller import OffboardController
from MissionComputer.telemetry_manager import TelemetryManager


class FlightManager:

    def __init__(self):

        self.drone = System()

        self.offboard = OffboardController(self.drone)

        self.telemetry = TelemetryManager(self.drone)

    async def connect(self):

        print("[MISSION] Connecting to PX4...")

        await self.drone.connect(
            system_address="udpin://0.0.0.0:14540"
        )

        async for state in self.drone.core.connection_state():

            if state.is_connected:

                print("[MISSION] Connected")
                break

    async def wait_until_ready(self):

        print("[MISSION] Waiting for vehicle health...")

        async for health in self.drone.telemetry.health():

            if (
                health.is_global_position_ok
                and
                health.is_home_position_ok
            ):

                print("[MISSION] Vehicle Ready")
                return

    async def arm(self):

        print("[MISSION] Arming...")

        await self.drone.action.arm()

        print("[MISSION] Armed")

    async def disarm(self):

        print("[MISSION] Disarming...")

        try:

            await self.drone.action.disarm()

        except Exception:

            pass

    async def takeoff(self, altitude):

        print(
            f"[MISSION] Setting takeoff altitude to {altitude} m..."
        )

        await self.drone.action.set_takeoff_altitude(
            altitude
        )

        print("[MISSION] Taking off...")

        await self.drone.action.takeoff()

    async def land(self):

        print("[MISSION] Landing...")

        await self.drone.action.land()
