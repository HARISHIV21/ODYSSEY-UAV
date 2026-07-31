class WaypointTracker:

    def __init__(self, mission):

        self.waypoints = mission["waypoints"]

        self.current = 0

    def total(self):

        return len(self.waypoints)

    def has_next(self):

        return self.current < len(self.waypoints)

    def current_waypoint(self):

        return self.waypoints[self.current]

    def advance(self):

        self.current += 1

    def remaining(self):

        return len(self.waypoints) - self.current
