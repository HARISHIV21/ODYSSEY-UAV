import json
from pathlib import Path


class MissionLoader:

    def __init__(self):

        self.mission_file = (
            Path(__file__).resolve().parent.parent
            / "Data"
            / "mission.json"
        )

    def load(self):

        if not self.mission_file.exists():

            raise FileNotFoundError(
                f"Mission file not found: {self.mission_file}"
            )

        with open(self.mission_file, "r") as file:

            mission = json.load(file)

        self.validate(mission)

        return mission

    def validate(self, mission):

        required = [
            "mission_name",
            "takeoff_altitude",
            "waypoints"
        ]

        for key in required:

            if key not in mission:

                raise ValueError(
                    f"Missing mission field: {key}"
                )

        if len(mission["waypoints"]) == 0:

            raise ValueError(
                "Mission contains no waypoints."
            )

        for i, wp in enumerate(mission["waypoints"], start=1):

            for key in [
                "north",
                "east",
                "down"
            ]:

                if key not in wp:

                    raise ValueError(
                        f"Waypoint {i} missing '{key}'"
                    )

    def print_summary(self, mission):

        print("\nMission Loaded")
        print("------------------------")
        print(
            f"Mission : {mission['mission_name']}"
        )
        print(
            f"Waypoints : {len(mission['waypoints'])}"
        )
