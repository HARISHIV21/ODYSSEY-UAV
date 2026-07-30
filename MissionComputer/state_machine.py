from enum import Enum, auto


class MissionState(Enum):
    INITIALIZE = auto()
    CONNECT = auto()
    WAIT_FOR_HEALTH = auto()
    ARM = auto()
    TAKEOFF = auto()
    START_OFFBOARD = auto()
    MISSION = auto()
    WAYPOINT = auto()
    RETURN_HOME = auto()
    LAND = auto()
    DISARM = auto()
    COMPLETE = auto()
    FAILSAFE = auto()
    ABORT = auto()


class StateMachine:

    def __init__(self):
        self.state = MissionState.INITIALIZE

    def set_state(self, new_state: MissionState):

        old = self.state
        self.state = new_state

        print(
            f"[STATE] {old.name}  --->  {new_state.name}"
        )

    def get_state(self):

        return self.state

    def is_complete(self):

        return self.state == MissionState.COMPLETE

    def is_failed(self):

        return self.state in (
            MissionState.FAILSAFE,
            MissionState.ABORT,
        )

    def reset(self):

        self.state = MissionState.INITIALIZE
