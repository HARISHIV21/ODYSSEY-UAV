import asyncio

from MissionComputer.flight_manager import FlightManager
from MissionComputer.mission_computer import MissionComputer
from Navigation.mission_loader import MissionLoader


async def main():

    loader = MissionLoader()
    mission = loader.load()

    loader.print_summary(mission)

    fm = FlightManager()

    # Connect first
    await fm.connect()

    mc = MissionComputer(
        fm,
        mission
    )

    # Now telemetry is available
    await mc.health_report()
    await mc.battery_report()

    await mc.start()

    print("\n==============================")
    print("ODYSSEY UAV MISSION FINISHED")
    print("==============================")


if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\nMission Interrupted")
