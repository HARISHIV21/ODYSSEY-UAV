class MissionPlanner:

    def __init__(self):
        self.waypoints = []

    def load(self, mission):

        self.waypoints.clear()

        for wp in mission["waypoints"]:
            self.waypoints.append(
                (
                    wp["x"],
                    wp["y"],
                    wp["z"]
                )
            )

    def show(self):

        print("\nMission Plan")

        for i, wp in enumerate(self.waypoints):
            print(f"{i+1}. {wp}")
