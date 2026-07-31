import json

from Navigation.mission_planner import MissionPlanner


class MissionLoader:

    def __init__(self):

        self.planner = MissionPlanner()

    def load(self):

        with open("Data/mission.json", "r") as f:

            mission = json.load(f)

        self.planner.load(mission)

        return mission

    def planner_instance(self):

        return self.planner

    def print_summary(self, mission):

        print("\nMission Loaded")
        print("------------------------")
        print(f"Mission : {mission['mission_name']}")
        print(f"Waypoints : {len(mission['waypoints'])}")

        self.planner.show()
