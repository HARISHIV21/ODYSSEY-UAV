from pathlib import Path

import pytest

from Navigation.mission_loader import MissionLoader


PROJECT_ROOT = Path(__file__).resolve().parent
MISSION_FILE = PROJECT_ROOT / "Data" / "mission.json"


def test_mission_loads_successfully():
    loader = MissionLoader(MISSION_FILE)

    mission = loader.load()

    assert mission["mission_name"] == "Square Flight"
    assert len(mission["waypoints"]) == 4


def test_waypoints_use_ned_coordinates():
    loader = MissionLoader(MISSION_FILE)

    loader.load()
    planner = loader.planner_instance()

    assert planner.total_waypoints() == 4

    first_waypoint = planner.get_waypoint(0)

    assert first_waypoint == {
        "north": 5,
        "east": 0,
        "down": -10
    }


def test_all_waypoints_have_valid_ned_fields():
    loader = MissionLoader(MISSION_FILE)

    mission = loader.load()

    for waypoint in mission["waypoints"]:
        assert "north" in waypoint
        assert "east" in waypoint
        assert "down" in waypoint


def test_missing_mission_file_raises_error():
    loader = MissionLoader(PROJECT_ROOT / "Data" / "missing.json")

    with pytest.raises(FileNotFoundError):
        loader.load()


def test_missing_waypoint_coordinate_is_rejected():
    from Navigation.mission_validator import (
        MissionValidator,
        MissionValidationError,
    )

    mission = {
        "mission_name": "Invalid Mission",
        "takeoff_altitude": 10,
        "waypoints": [{"north": 5, "east": 0}],
    }

    with pytest.raises(MissionValidationError, match="down"):
        MissionValidator.validate(mission)


def test_invalid_takeoff_altitude_is_rejected():
    from Navigation.mission_validator import (
        MissionValidator,
        MissionValidationError,
    )

    mission = {
        "mission_name": "Invalid Mission",
        "takeoff_altitude": -5,
        "waypoints": [{"north": 5, "east": 0, "down": -10}],
    }

    with pytest.raises(MissionValidationError, match="takeoff_altitude"):
        MissionValidator.validate(mission)


def test_empty_waypoint_list_is_rejected():
    from Navigation.mission_validator import (
        MissionValidator,
        MissionValidationError,
    )

    mission = {
        "mission_name": "Empty Mission",
        "takeoff_altitude": 10,
        "waypoints": [],
    }

    with pytest.raises(MissionValidationError, match="at least one"):
        MissionValidator.validate(mission)


def test_non_numeric_coordinate_is_rejected():
    from Navigation.mission_validator import (
        MissionValidator,
        MissionValidationError,
    )

    mission = {
        "mission_name": "Invalid Mission",
        "takeoff_altitude": 10,
        "waypoints": [{"north": "five", "east": 0, "down": -10}],
    }

    with pytest.raises(MissionValidationError, match="must be a number"):
        MissionValidator.validate(mission)


def test_non_finite_coordinate_is_rejected():
    from Navigation.mission_validator import (
        MissionValidator,
        MissionValidationError,
    )

    mission = {
        "mission_name": "Invalid Mission",
        "takeoff_altitude": 10,
        "waypoints": [{"north": float("nan"), "east": 0, "down": -10}],
    }

    with pytest.raises(MissionValidationError, match="must be finite"):
        MissionValidator.validate(mission)


def test_px4_connection_is_not_repeated():
    import asyncio
    from types import SimpleNamespace
    from MissionComputer.flight_manager import FlightManager

    class FakeCore:
        async def connection_state(self):
            yield SimpleNamespace(is_connected=True)

    class FakeDrone:
        def __init__(self):
            self.connect_calls = 0
            self.core = FakeCore()

        async def connect(self, system_address):
            self.connect_calls += 1

    manager = FlightManager.__new__(FlightManager)
    manager._connected = False
    manager.connection_timeout = 15.0
    manager.drone = FakeDrone()

    async def run_test():
        await manager.connect()
        await manager.connect()

    asyncio.run(run_test())

    assert manager.drone.connect_calls == 1
    assert manager._connected is True


def test_px4_connection_failure_is_reported():
    import asyncio
    from MissionComputer.flight_manager import FlightManager

    class FakeCore:
        async def connection_state(self):
            if False:
                yield None

    class FakeDrone:
        def __init__(self):
            self.core = FakeCore()

        async def connect(self, system_address):
            pass

    manager = FlightManager.__new__(FlightManager)
    manager._connected = False
    manager.connection_timeout = 15.0
    manager.drone = FakeDrone()

    with pytest.raises(RuntimeError, match="connection state stream ended"):
        asyncio.run(manager.connect())

    assert manager._connected is False


def test_px4_connection_timeout_is_reported():
    import asyncio
    from types import SimpleNamespace
    from MissionComputer.flight_manager import FlightManager

    class FakeCore:
        async def connection_state(self):
            await asyncio.sleep(1)
            yield SimpleNamespace(is_connected=True)

    class FakeDrone:
        def __init__(self):
            self.core = FakeCore()

        async def connect(self, system_address):
            pass

    manager = FlightManager.__new__(FlightManager)
    manager._connected = False
    manager.connection_timeout = 15.0
    manager.connection_timeout = 0.05
    manager.drone = FakeDrone()

    with pytest.raises(TimeoutError, match="timed out"):
        asyncio.run(manager.connect())

    assert manager._connected is False


def test_wait_until_landed_accepts_on_ground():
    import asyncio
    from mavsdk.telemetry import LandedState
    from MissionComputer.flight_manager import FlightManager

    class FakeTelemetry:
        async def landed_state(self):
            yield LandedState.ON_GROUND

    manager = FlightManager.__new__(FlightManager)
    manager.drone = type(
        "FakeDrone", (), {"telemetry": FakeTelemetry()}
    )()

    assert asyncio.run(manager.wait_until_landed(timeout=1.0)) is True


def test_wait_until_landed_waits_through_airborne_state():
    import asyncio
    from mavsdk.telemetry import LandedState
    from MissionComputer.flight_manager import FlightManager

    class FakeTelemetry:
        async def landed_state(self):
            yield LandedState.IN_AIR
            yield LandedState.LANDING
            yield LandedState.ON_GROUND

    manager = FlightManager.__new__(FlightManager)
    manager.drone = type(
        "FakeDrone", (), {"telemetry": FakeTelemetry()}
    )()

    assert asyncio.run(manager.wait_until_landed(timeout=1.0)) is True


def test_wait_until_landed_times_out():
    import asyncio
    from mavsdk.telemetry import LandedState
    from MissionComputer.flight_manager import FlightManager

    class FakeTelemetry:
        async def landed_state(self):
            while True:
                yield LandedState.IN_AIR
                await asyncio.sleep(0.1)

    manager = FlightManager.__new__(FlightManager)
    manager.drone = type(
        "FakeDrone", (), {"telemetry": FakeTelemetry()}
    )()

    with pytest.raises(TimeoutError, match="landing confirmation"):
        asyncio.run(manager.wait_until_landed(timeout=0.05))


def test_wait_until_landed_rejects_ended_stream():
    import asyncio
    from MissionComputer.flight_manager import FlightManager

    class FakeTelemetry:
        async def landed_state(self):
            if False:
                yield None

    manager = FlightManager.__new__(FlightManager)
    manager.drone = type(
        "FakeDrone", (), {"telemetry": FakeTelemetry()}
    )()

    with pytest.raises(RuntimeError, match="stream ended"):
        asyncio.run(manager.wait_until_landed(timeout=1.0))


def test_disarm_errors_are_not_silently_ignored():
    import asyncio
    from MissionComputer.flight_manager import FlightManager

    class FakeAction:
        async def disarm(self):
            raise RuntimeError("Disarm rejected")

    manager = FlightManager.__new__(FlightManager)
    manager.drone = type(
        "FakeDrone", (), {"action": FakeAction()}
    )()

    with pytest.raises(RuntimeError, match="Disarm rejected"):
        asyncio.run(manager.disarm())


def test_wait_until_disarmed_accepts_disarmed_state():
    import asyncio
    from MissionComputer.flight_manager import FlightManager

    class FakeTelemetry:
        async def armed(self):
            yield False

    manager = FlightManager.__new__(FlightManager)
    manager.drone = type(
        "FakeDrone", (), {"telemetry": FakeTelemetry()}
    )()

    assert asyncio.run(manager.wait_until_disarmed(timeout=1.0)) is True


def test_wait_until_disarmed_waits_for_armed_state_to_clear():
    import asyncio
    from MissionComputer.flight_manager import FlightManager

    class FakeTelemetry:
        async def armed(self):
            yield True
            yield False

    manager = FlightManager.__new__(FlightManager)
    manager.drone = type(
        "FakeDrone", (), {"telemetry": FakeTelemetry()}
    )()

    assert asyncio.run(manager.wait_until_disarmed(timeout=1.0)) is True


def test_wait_until_disarmed_times_out():
    import asyncio
    from MissionComputer.flight_manager import FlightManager

    class FakeTelemetry:
        async def armed(self):
            while True:
                yield True
                await asyncio.sleep(0.1)

    manager = FlightManager.__new__(FlightManager)
    manager.drone = type(
        "FakeDrone", (), {"telemetry": FakeTelemetry()}
    )()

    with pytest.raises(TimeoutError, match="disarm confirmation"):
        asyncio.run(manager.wait_until_disarmed(timeout=0.05))


def test_wait_until_disarmed_rejects_ended_stream():
    import asyncio
    from MissionComputer.flight_manager import FlightManager

    class FakeTelemetry:
        async def armed(self):
            if False:
                yield None

    manager = FlightManager.__new__(FlightManager)
    manager.drone = type(
        "FakeDrone", (), {"telemetry": FakeTelemetry()}
    )()

    with pytest.raises(RuntimeError, match="stream ended"):
        asyncio.run(manager.wait_until_disarmed(timeout=1.0))


def test_wait_until_disarmed_rejects_invalid_timeout():
    import asyncio
    from MissionComputer.flight_manager import FlightManager

    manager = FlightManager.__new__(FlightManager)

    with pytest.raises(ValueError, match="timeout"):
        asyncio.run(manager.wait_until_disarmed(timeout=0))


class FakeMissionOffboard:
    async def start(self, altitude):
        pass

    async def goto(self, north, east, down, yaw):
        pass

    async def stop(self):
        pass


class FakeMissionFlightManager:
    def __init__(self):
        self.drone = object()
        self.offboard = FakeMissionOffboard()
        self.events = []

    async def connect(self):
        self.events.append("connect")

    async def wait_until_ready(self):
        self.events.append("ready")

    async def arm(self):
        self.events.append("arm")

    async def takeoff(self, altitude):
        self.events.append("takeoff")

    async def land(self):
        self.events.append("land")

    async def wait_until_landed(self, timeout):
        self.events.append("landed")

    async def wait_until_disarmed(self, timeout):
        self.events.append("disarmed")

    async def disarm(self):
        self.events.append("disarm")


class FakeMissionNavigator:
    async def wait_until_arrived(self, waypoint):
        return True


def create_test_mission_manager():
    from MissionComputer.mission_manager import MissionManager
    from MissionComputer.state_machine import StateMachine

    mission = {
        "takeoff_altitude": 5.0,
        "waypoints": [
            {"north": 5.0, "east": 0.0, "down": -5.0}
        ],
    }

    flight_manager = FakeMissionFlightManager()
    manager = MissionManager(flight_manager, mission)
    manager.navigator = FakeMissionNavigator()

    state_machine = StateMachine()
    manager.attach_state_machine(state_machine)

    return manager, flight_manager, state_machine


def test_mission_completes_only_after_landing_and_disarming():
    import asyncio
    from MissionComputer.state_machine import MissionState

    manager, flight_manager, state_machine = create_test_mission_manager()

    asyncio.run(manager.run())

    assert state_machine.get_state() == MissionState.COMPLETE
    assert flight_manager.events.index("landed") < flight_manager.events.index("disarmed")


def test_mission_does_not_complete_if_landing_fails():
    import asyncio
    from MissionComputer.state_machine import MissionState

    manager, flight_manager, state_machine = create_test_mission_manager()

    async def landing_failure(timeout):
        flight_manager.events.append("landing_failed")
        raise TimeoutError("Landing not confirmed")

    flight_manager.wait_until_landed = landing_failure

    with pytest.raises(TimeoutError, match="Landing not confirmed"):
        asyncio.run(manager.run())

    assert state_machine.get_state() != MissionState.COMPLETE
    assert "disarmed" not in flight_manager.events


def test_mission_does_not_complete_if_disarming_fails():
    import asyncio
    from MissionComputer.state_machine import MissionState

    manager, flight_manager, state_machine = create_test_mission_manager()

    async def disarm_failure(timeout):
        flight_manager.events.append("disarm_failed")
        raise RuntimeError("Disarm telemetry unavailable")

    flight_manager.wait_until_disarmed = disarm_failure

    with pytest.raises(RuntimeError, match="Disarm telemetry unavailable"):
        asyncio.run(manager.run())

    assert state_machine.get_state() != MissionState.COMPLETE


def test_failsafe_rejects_unavailable_battery_telemetry():
    import asyncio
    from MissionComputer.failsafe_manager import FailsafeManager
    from MissionComputer.state_machine import MissionState

    class Battery:
        async def is_low(self, threshold):
            raise RuntimeError("Battery telemetry lost")

    class Health:
        async def check(self):
            return True

    manager = FailsafeManager(object(), Battery(), Health())

    assert asyncio.run(manager.check_battery()) is False
    assert manager.reason == "BATTERY TELEMETRY FAILURE"


def test_failsafe_rejects_unavailable_health_telemetry():
    import asyncio
    from MissionComputer.failsafe_manager import FailsafeManager

    class Battery:
        async def is_low(self, threshold):
            return False

    class Health:
        async def check(self):
            raise RuntimeError("Health telemetry lost")

    manager = FailsafeManager(object(), Battery(), Health())

    assert asyncio.run(manager.check_health()) is False
    assert manager.reason == "VEHICLE HEALTH TELEMETRY FAILURE"


def test_failsafe_confirms_landing_before_disarming(capsys):
    import asyncio
    from MissionComputer.failsafe_manager import FailsafeManager

    class Offboard:
        async def stop(self):
            events.append("offboard_stop")

    class FlightManager:
        def __init__(self):
            self.offboard = Offboard()

        async def land(self):
            events.append("land")

        async def wait_until_landed(self, timeout):
            events.append("landed")

        async def wait_until_disarmed(self, timeout):
            events.append("disarmed")

        async def disarm(self):
            events.append("unsafe_disarm")

    events = []
    manager = FailsafeManager(FlightManager(), object(), object())
    manager.reason = "TEST FAILURE"

    asyncio.run(manager.execute())

    assert events == [
        "offboard_stop",
        "land",
        "landed",
        "disarmed",
    ]
    assert "VEHICLE SAFE" in capsys.readouterr().out


def test_failsafe_never_disarms_if_landing_is_unconfirmed(capsys):
    import asyncio
    from MissionComputer.failsafe_manager import FailsafeManager

    events = []

    class Offboard:
        async def stop(self):
            events.append("offboard_stop")

    class FlightManager:
        offboard = Offboard()

        async def land(self):
            events.append("land")

        async def wait_until_landed(self, timeout):
            events.append("landing_failed")
            raise TimeoutError("Landing not confirmed")

        async def wait_until_disarmed(self, timeout):
            events.append("disarmed")

        async def disarm(self):
            events.append("unsafe_disarm")

    manager = FailsafeManager(FlightManager(), object(), object())
    manager.reason = "TEST LANDING FAILURE"

    asyncio.run(manager.execute())

    assert "unsafe_disarm" not in events
    assert "disarmed" not in events
    assert "LANDING STATUS UNKNOWN" in capsys.readouterr().out


def test_failsafe_does_not_report_safe_if_disarming_fails(capsys):
    import asyncio
    from MissionComputer.failsafe_manager import FailsafeManager

    class Offboard:
        async def stop(self):
            pass

    class FlightManager:
        offboard = Offboard()

        async def land(self):
            pass

        async def wait_until_landed(self, timeout):
            pass

        async def wait_until_disarmed(self, timeout):
            raise RuntimeError("Disarm telemetry unavailable")

        async def disarm(self):
            raise RuntimeError("Disarm command failed")

    manager = FailsafeManager(FlightManager(), object(), object())
    manager.reason = "TEST DISARM FAILURE"

    asyncio.run(manager.execute())

    output = capsys.readouterr().out
    assert "LANDING CONFIRMED - DISARM UNCONFIRMED" in output
    assert "VEHICLE SAFE" not in output


def test_executor_propagates_failure_without_duplicate_landing():
    import asyncio
    from types import SimpleNamespace
    from MissionComputer.mission_executor import MissionExecutor
    from MissionComputer.state_machine import MissionState

    events = []

    class MissionManager:
        state_machine = SimpleNamespace(
            set_state=lambda state: events.append(("state", state))
        )

        async def run(self):
            raise RuntimeError("Waypoint navigation failed")

    class FlightManager:
        offboard = SimpleNamespace(
            stop=lambda: events.append(("offboard_stop",))
        )

        async def land(self):
            events.append(("land",))

    executor = MissionExecutor(FlightManager(), MissionManager())

    with pytest.raises(RuntimeError, match="Waypoint navigation failed"):
        asyncio.run(executor.execute())

    assert ("state", MissionState.FAILSAFE) in events
    assert ("offboard_stop",) not in events
    assert ("land",) not in events


def test_executor_propagates_cancellation_without_failsafe():
    import asyncio
    from types import SimpleNamespace
    from MissionComputer.mission_executor import MissionExecutor
    from MissionComputer.state_machine import MissionState

    events = []

    class MissionManager:
        state_machine = SimpleNamespace(
            set_state=lambda state: events.append(state)
        )

        async def run(self):
            raise asyncio.CancelledError()

    executor = MissionExecutor(object(), MissionManager())

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(executor.execute())

    assert MissionState.FAILSAFE not in events


def test_navigation_confirms_waypoint_arrival():
    import asyncio
    from types import SimpleNamespace
    from Navigation.navigation_engine import NavigationEngine

    class Telemetry:
        async def position_velocity_ned(self):
            position = SimpleNamespace(
                north_m=5, east_m=0, down_m=-10
            )
            yield SimpleNamespace(position=position)

    drone = SimpleNamespace(telemetry=Telemetry())
    navigator = NavigationEngine(drone)

    result = asyncio.run(navigator.wait_until_arrived(
        {"north": 5, "east": 0, "down": -10}
    ))
    assert result is True


def test_navigation_fails_if_telemetry_stream_ends():
    import asyncio
    from types import SimpleNamespace
    from Navigation.navigation_engine import NavigationEngine

    class Telemetry:
        async def position_velocity_ned(self):
            if False:
                yield None

    navigator = NavigationEngine(
        SimpleNamespace(telemetry=Telemetry())
    )

    with pytest.raises(RuntimeError, match="telemetry"):
        asyncio.run(navigator.wait_until_arrived(
            {"north": 5, "east": 0, "down": -10}
        ))


def test_navigation_rejects_invalid_timeout():
    import asyncio
    from types import SimpleNamespace
    from Navigation.navigation_engine import NavigationEngine

    navigator = NavigationEngine(
        SimpleNamespace(telemetry=None)
    )

    with pytest.raises(ValueError):
        asyncio.run(navigator.wait_until_arrived(
            {"north": 5, "east": 0, "down": -10},
            timeout=0
        ))


def test_telemetry_update_rejects_empty_position_stream():
    import asyncio
    from types import SimpleNamespace
    from MissionComputer.telemetry_manager import TelemetryManager

    class Telemetry:
        async def position_velocity_ned(self):
            if False:
                yield None

        async def battery(self):
            yield SimpleNamespace(remaining_percent=90.0)

        async def flight_mode(self):
            yield "OFFBOARD"

    manager = TelemetryManager(
        SimpleNamespace(telemetry=Telemetry())
    )

    with pytest.raises(RuntimeError, match="position"):
        asyncio.run(manager.update())


def test_telemetry_update_rejects_empty_battery_stream():
    import asyncio
    from types import SimpleNamespace
    from MissionComputer.telemetry_manager import TelemetryManager

    class Telemetry:
        async def position_velocity_ned(self):
            position = SimpleNamespace(
                north_m=1.0, east_m=2.0, down_m=-3.0
            )
            yield SimpleNamespace(position=position)

        async def battery(self):
            if False:
                yield None

        async def flight_mode(self):
            yield "OFFBOARD"

    manager = TelemetryManager(
        SimpleNamespace(telemetry=Telemetry())
    )

    with pytest.raises(RuntimeError, match="battery"):
        asyncio.run(manager.update())
