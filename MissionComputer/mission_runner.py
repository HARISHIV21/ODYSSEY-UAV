import asyncio
import json
from flight_manager import FlightManager


def load_mission(path):
    with open(path, "r") as f:
        return json.load(f)


async def main():

    mission = load_mission("../Data/Missions/mission.json")

    fm = FlightManager()

    await fm.connect()
    await fm.wait_until_ready()

    print("[MISSION] Arming...")
    await fm.arm()

    print("[MISSION] Taking off...")
    await fm.takeoff()

    print(f"[MISSION] Loaded mission: {mission['mission_name']}")

    for i, wp in enumerate(mission["waypoints"], start=1):
        print(
            f"[MISSION] Waypoint {i}: "
            f"({wp['x']}, {wp['y']}, {wp['z']})"
        )

        # Placeholder for actual navigation
        await asyncio.sleep(5)

    print("[MISSION] Landing...")
    await fm.land()

    print("[MISSION] Complete")


if __name__ == "__main__":
    asyncio.run(main())

