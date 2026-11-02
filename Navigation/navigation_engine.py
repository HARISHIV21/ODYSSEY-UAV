import asyncio
import math

from Navigation.distance import DistanceCalculator


class NavigationEngine:

    def __init__(self, drone, tolerance=1.0):
        self.drone = drone
        self.tolerance = tolerance
        self.distance = DistanceCalculator()

    async def wait_until_arrived(self, target, timeout=60.0):

        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or not math.isfinite(timeout)
            or timeout <= 0
        ):
            raise ValueError("Navigation timeout must be a positive finite number")

        print(
            f"[NAV] Tracking waypoint "
            f"N:{target['north']} "
            f"E:{target['east']} "
            f"D:{target['down']}"
        )

        try:
            async with asyncio.timeout(timeout):
                async for data in self.drone.telemetry.position_velocity_ned():

                    current = data.position

                    distance_3d = self.distance.distance_3d(
                        current, target
                    )

                    horizontal = self.distance.horizontal(
                        current, target
                    )

                    vertical = self.distance.vertical(
                        current, target
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

        except TimeoutError as exc:
            raise TimeoutError(
                f"Waypoint arrival not confirmed within {timeout} seconds"
            ) from exc

        raise RuntimeError(
            "Position telemetry stream ended before waypoint arrival"
        )
