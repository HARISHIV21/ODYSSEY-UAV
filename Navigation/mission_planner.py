class MissionPlanner:

    def __init__(self):
        self.waypoints = []

    def load(self, mission):

        self.waypoints.clear()

        for wp in mission["waypoints"]:
            self.waypoints.append(
                {
                    "north": wp["north"],
                    "east": wp["east"],
                    "down": wp["down"]
                }
            )

    def total_waypoints(self):

        return len(self.waypoints)

    def get_waypoint(self, index):

        return self.waypoints[index]

    def show(self):

        print("\n========== MISSION PLAN ==========")

        for i, wp in enumerate(self.waypoints):

            print(
                f"{i+1}. "
                f"N:{wp['north']}  "
                f"E:{wp['east']}  "
                f"D:{wp['down']}"
            )

        print("==================================")
