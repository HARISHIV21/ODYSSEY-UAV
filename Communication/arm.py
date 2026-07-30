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

    print("Waiting for health...")

    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("✅ Drone Ready")
            break

    print("Arming...")

    await drone.action.arm()

    print("✅ Drone Armed")


if __name__ == "__main__":
    asyncio.run(main())
