from enum import Enum


class UAVState(Enum):
    IDLE = 0
    INITIALIZING = 1
    CONNECTED = 2
    ARMED = 3
    TAKEOFF = 4
    MISSION = 5
    RTL = 6
    LANDING = 7
    COMPLETE = 8


class MissionCore:

    def __init__(self):
        self.state = UAVState.IDLE

    def change_state(self, state):
        print(f"[CORE] {self.state.name} -> {state.name}")
        self.state = state

    def initialize(self):
        self.change_state(UAVState.INITIALIZING)

    def connect(self):
        self.change_state(UAVState.CONNECTED)

    def arm(self):
        self.change_state(UAVState.ARMED)

    def takeoff(self):
        self.change_state(UAVState.TAKEOFF)

    def mission(self):
        self.change_state(UAVState.MISSION)

    def rtl(self):
        self.change_state(UAVState.RTL)

    def land(self):
        self.change_state(UAVState.LANDING)

    def finish(self):
        self.change_state(UAVState.COMPLETE)


if __name__ == "__main__":
    core = MissionCore()

    core.initialize()
    core.connect()
    core.arm()
    core.takeoff()
    core.mission()
    core.rtl()
    core.land()
    core.finish()
