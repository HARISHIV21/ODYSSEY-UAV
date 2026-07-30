import asyncio
from flight_manager import FlightManager


async def main():

    manager = FlightManager()

    await manager.connect()

    await manager.wait_until_ready()

    await manager.arm()

    await manager.takeoff()

    print("Hovering for 10 seconds...")

    await asyncio.sleep(10)

    await manager.land()


asyncio.run(main())
