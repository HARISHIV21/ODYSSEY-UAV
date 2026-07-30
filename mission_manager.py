from MissionComputer.state_machine import MissionState


class MissionManager:

    def __init__(self, flight_manager, mission):

        self.fm = flight_manager
        self.mission = mission
        self.state_machine = None

    def attach_state_machine(self, state_machine):

        self.state_machine = state_machine

    async def run(self):

        sm = self.state_machine

        sm.set_state(MissionState.CONNECT)
        await self.fm.connect()

        sm.set_state(MissionState.WAIT_FOR_HEALTH)
        await self.fm.wait_until_ready()

        sm.set_state(MissionState.ARM)
        await self.fm.arm()

        sm.set_state(MissionState.TAKEOFF)
        await self.fm.takeoff(
            self.mission["takeoff_altitude"]
        )

        sm.set_state(MissionState.START_OFFBOARD)
        await self.fm.offboard.start(
            self.mission["takeoff_altitude"]
        )

        sm.set_state(MissionState.MISSION)

        waypoints = self.mission["waypoints"]

        for index, wp in enumerate(waypoints, start=1):

            sm.set_state(MissionState.WAYPOINT)

            print(
                f"\n[MISSION] Waypoint {index}/{len(waypoints)}"
            )

            await self.fm.offboard.goto(
                wp["north"],
                wp["east"],
                wp["down"],
                wp.get("yaw", 0),
            )

        sm.set_state(MissionState.LAND)

        await self.fm.offboard.stop()

        await self.fm.land()

        sm.set_state(MissionState.DISARM)

        try:
            await self.fm.disarm()
        except Exception:
            pass

        sm.set_state(MissionState.COMPLETE)

        print("\n==============================")
        print("MISSION COMPLETE")
        print("==============================")
