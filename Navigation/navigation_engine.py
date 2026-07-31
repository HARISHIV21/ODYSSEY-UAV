import asyncio

from Navigation.distance import DistanceCalculator


class NavigationEngine:

    def __init__(self, drone, tolerance=1.0):

        self.drone = drone
        self.tolerance = tolerance

        self.distance = DistanceCalculator()

    async def wait_until_arrived(self, target):

        print(
            f"[NAV] Tracking waypoint "
            f"N:{target['north']} "
            f"E:{target['east']} "
            f"D:{target['down']}"
        )

        async for data in self.drone.telemetry.position_velocity_ned():

            current = data.position

            distance_3d = self.distance.distance_3d(
                current,
                target
            )

            horizontal = self.distance.horizontal(
                current,
                target
            )

            vertical = self.distance.vertical(
                current,
                target
            )

            print(
                f"[NAV] Distance: {distance_3d:.2f} m | "
                f"Horizontal: {horizontal:.2f} m | "
                f"Vertical: {vertical:.2f} m"
            )

            if distance_3d <= self.tolerance:

                print(
                    f"[NAV] Waypoint reached "
                    f"({distance_3d:.2f} m)"
                )

                return True

            await asyncio.sleep(0.2)
