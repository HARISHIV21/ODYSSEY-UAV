import asyncio
from mavsdk import System


async def main():
    drone = System()

    await drone.connect(system_address="udpin://0.0.0.0:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            break

    print("Landing...")
    await drone.action.land()

    print("Land command sent")


if __name__ == "__main__":
    asyncio.run(main())
