from MissionComputer.state_machine import MissionState
from Navigation.navigation_engine import NavigationEngine
from Navigation.waypoint_tracker import WaypointTracker


class MissionManager:

    def __init__(self, flight_manager, mission):

        self.fm = flight_manager
        self.mission = mission
        self.state_machine = None

        # Navigation engine confirms real waypoint arrival
        self.navigator = NavigationEngine(
            self.fm.drone,
            tolerance=1.0
        )

        # Tracks mission completion/progress
        self.tracker = WaypointTracker(
            mission
        )

    def attach_state_machine(self, state_machine):

        self.state_machine = state_machine

    async def run(self):

        sm = self.state_machine

        # -------------------------------------------------
        # CONNECT
        # -------------------------------------------------

        sm.set_state(MissionState.CONNECT)
        await self.fm.connect()

        # -------------------------------------------------
        # VEHICLE HEALTH
        # -------------------------------------------------

        sm.set_state(MissionState.WAIT_FOR_HEALTH)
        await self.fm.wait_until_ready()

        # -------------------------------------------------
        # ARM
        # -------------------------------------------------

        sm.set_state(MissionState.ARM)
        await self.fm.arm()

        # -------------------------------------------------
        # TAKEOFF
        # -------------------------------------------------

        sm.set_state(MissionState.TAKEOFF)

        await self.fm.takeoff(
            self.mission["takeoff_altitude"]
        )

        # -------------------------------------------------
        # START OFFBOARD
        # -------------------------------------------------

        sm.set_state(MissionState.START_OFFBOARD)

        await self.fm.offboard.start(
            self.mission["takeoff_altitude"]
        )

        # -------------------------------------------------
        # MISSION
        # -------------------------------------------------

        sm.set_state(MissionState.MISSION)

        print("\n========== MISSION PROGRESS ==========")
        print(
            f"Completed : 0/{self.tracker.total()}"
        )
        print(
            f"Remaining : {self.tracker.remaining()}"
        )
        print("Progress  : 0.0%")
        print("======================================")

        # -------------------------------------------------
        # WAYPOINT EXECUTION
        # -------------------------------------------------

        while self.tracker.has_next():

            wp = self.tracker.current_waypoint()

            waypoint_number = self.tracker.completed() + 1

            sm.set_state(MissionState.WAYPOINT)

            print(
                f"\n[MISSION] Waypoint "
                f"{waypoint_number}/{self.tracker.total()}"
            )

            print(
                f"[MISSION] Target -> "
                f"N:{wp['north']} "
                f"E:{wp['east']} "
                f"D:{wp['down']}"
            )

            # Send waypoint to PX4 offboard controller
            await self.fm.offboard.goto(
                wp["north"],
                wp["east"],
                wp["down"],
                wp.get("yaw", 0),
            )

            # Confirm vehicle physically reached waypoint
            await self.navigator.wait_until_arrived(
                wp
            )

            # Waypoint completed
            self.tracker.advance()

            # Print progress
            self.tracker.print_progress()

        # -------------------------------------------------
        # LAND
        # -------------------------------------------------

        sm.set_state(MissionState.LAND)

        await self.fm.offboard.stop()

        await self.fm.land()

        # Wait for PX4 to confirm that the vehicle is physically on ground.
        await self.fm.wait_until_landed(timeout=60.0)

        # -------------------------------------------------
        # DISARM
        # -------------------------------------------------

        sm.set_state(MissionState.DISARM)

        # PX4 may automatically disarm after detecting landing.
        try:
            await self.fm.wait_until_disarmed(timeout=3.0)
        except TimeoutError:
            print("[MISSION] Still armed after landing; requesting disarm...")
            await self.fm.disarm()
            await self.fm.wait_until_disarmed(timeout=15.0)

        # -------------------------------------------------
        # COMPLETE
        # -------------------------------------------------

        sm.set_state(MissionState.COMPLETE)

        print("\n==============================")
        print("MISSION COMPLETE")
        print("==============================")

        print(
            f"Waypoints Completed : "
            f"{self.tracker.completed()}/{self.tracker.total()}"
        )

        print(
            f"Mission Progress     : "
            f"{self.tracker.progress():.1f}%"
        )

        print("==============================")
