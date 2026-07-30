import asyncio
from mavsdk import System


class UAVConnection:

    def __init__(self):
        self.drone = System()

    async def connect(self):
        print("[COMM] Connecting to PX4...")

        await self.drone.connect(
            system_address="udpin://0.0.0.0:14540"
        )

        async for state in self.drone.core.connection_state():

            if state.is_connected:
                print("[COMM] Connected to PX4")
                break

        return self.drone


async def main():

    connection = UAVConnection()

    await connection.connect()


if __name__ == "__main__":
    asyncio.run(main())
