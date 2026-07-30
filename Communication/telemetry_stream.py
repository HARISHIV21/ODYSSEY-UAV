import asyncio
from mavsdk import System


async def main():
    drone = System()

    print("Connecting...")

    await drone.connect(system_address="udpin://0.0.0.0:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected!")
            break

    print("Reading Telemetry...\n")

    async for health in drone.telemetry.health():
        print("GPS OK :", health.is_global_position_ok)
        print("Home OK:", health.is_home_position_ok)
        break

    async for position in drone.telemetry.position():
        print(f"Latitude : {position.latitude_deg:.6f}")
        print(f"Longitude: {position.longitude_deg:.6f}")
        print(f"Altitude : {position.relative_altitude_m:.2f}")
        print("-"*40)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
