from enum import Enum


class FlightMode(Enum):
    MANUAL = 0
    STABILIZED = 1
    ALTITUDE = 2
    POSITION = 3
    OFFBOARD = 4
    AUTO_MISSION = 5
    RTL = 6
    LAND = 7


class FlightModeManager:

    def __init__(self):
        self.mode = FlightMode.MANUAL

    def set_mode(self, mode):
        print(f"[MODE] {self.mode.name} -> {mode.name}")
        self.mode = mode


if __name__ == "__main__":

    manager = FlightModeManager()

    manager.set_mode(FlightMode.STABILIZED)
    manager.set_mode(FlightMode.POSITION)
    manager.set_mode(FlightMode.OFFBOARD)
    manager.set_mode(FlightMode.AUTO_MISSION)
    manager.set_mode(FlightMode.RTL)
    manager.set_mode(FlightMode.LAND)
