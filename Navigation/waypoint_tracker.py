class WaypointTracker:

    def __init__(self, mission):

        self.waypoints = mission["waypoints"]
        self.current = 0

    def total(self):

        return len(self.waypoints)

    def has_next(self):

        return self.current < self.total()

    def current_waypoint(self):

        if not self.has_next():
            return None

        return self.waypoints[self.current]

    def advance(self):

        if self.has_next():
            self.current += 1

    def completed(self):

        return self.current

    def remaining(self):

        return self.total() - self.current

    def progress(self):

        if self.total() == 0:
            return 100.0

        return (
            self.completed()
            / self.total()
        ) * 100.0

    def print_progress(self):

        print("\n========== MISSION PROGRESS ==========")

        print(
            f"Completed : {self.completed()}/{self.total()}"
        )

        print(
            f"Remaining : {self.remaining()}"
        )

        print(
            f"Progress  : {self.progress():.1f}%"
        )

        print("======================================")
