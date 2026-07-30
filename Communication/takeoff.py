import asyncio
from mavsdk import System


async def main():
    drone = System()

    print("Connecting to PX4...")
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("✅ Connected")
            break

    print("Waiting for vehicle health...")

    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("✅ Vehicle Ready")
            break

    print("Arming...")
    await drone.action.arm()

    print("Setting takeoff altitude...")
    await drone.action.set_takeoff_altitude(10.0)

    print("Taking off...")
    await drone.action.takeoff()

    print("Waiting 15 seconds...")

    await asyncio.sleep(15)

    print("Takeoff Complete")


if __name__ == "__main__":
    asyncio.run(main())
