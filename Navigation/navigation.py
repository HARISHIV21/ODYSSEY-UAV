import math


class Navigation:

    def __init__(self):

        self.current_position = (0.0, 0.0, 0.0)
        self.target_position = None

    def update_position(self, north, east, down):

        self.current_position = (north, east, down)

    def set_target(self, north, east, down):

        self.target_position = (north, east, down)

        print(
            f"[NAV] Target -> "
            f"N:{north:.2f} "
            f"E:{east:.2f} "
            f"D:{down:.2f}"
        )

    def distance_to_target(self):

        if self.target_position is None:
            return None

        n1, e1, d1 = self.current_position
        n2, e2, d2 = self.target_position

        return math.sqrt(
            (n2 - n1) ** 2 +
            (e2 - e1) ** 2 +
            (d2 - d1) ** 2
        )

    def reached_target(self, tolerance=0.5):

        distance = self.distance_to_target()

        if distance is None:
            return False

        return distance <= tolerance

    def status(self):

        print("\n========== NAVIGATION ==========")
        print(f"Current : {self.current_position}")
        print(f"Target  : {self.target_position}")

        if self.target_position is not None:
            print(
                f"Distance: "
                f"{self.distance_to_target():.2f} m"
            )

        print("================================")
