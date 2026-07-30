import sys

sys.path.extend([
    "Navigation"
])

from mission_loader import MissionLoader
from mission_planner import MissionPlanner


loader = MissionLoader("Data/Missions/mission.json")

mission = loader.load()

planner = MissionPlanner()

planner.load(mission)

planner.show()
