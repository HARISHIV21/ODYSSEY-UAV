import json
from pathlib import Path

from Navigation.mission_planner import MissionPlanner
from Navigation.mission_validator import MissionValidator


class MissionLoader:
    """Loads mission configuration from a JSON file."""

    def __init__(self, mission_path="Data/mission.json"):
        self.mission_path = Path(mission_path)
        self.planner = MissionPlanner()

    def load(self):
        if not self.mission_path.is_file():
            raise FileNotFoundError(
                f"Mission file not found: {self.mission_path}"
            )

        with self.mission_path.open("r", encoding="utf-8") as file:
            mission = json.load(file)

        MissionValidator.validate(mission)
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
