from MissionComputer.state_machine import StateMachine
from MissionComputer.mission_manager import MissionManager
from MissionComputer.mission_executor import MissionExecutor
from MissionComputer.battery_monitor import BatteryMonitor
from MissionComputer.health_monitor import HealthMonitor
from MissionComputer.failsafe_manager import FailsafeManager
from MissionComputer.logger import MissionLogger
from MissionComputer.flight_recorder import FlightRecorder


class MissionComputer:

    def __init__(self, flight_manager, mission):

        self.flight_manager = flight_manager
        self.mission = mission

        self.logger = MissionLogger()

        self.recorder = FlightRecorder()

        self.state_machine = StateMachine()

        self.battery = BatteryMonitor(
            flight_manager.drone
        )

        self.health = HealthMonitor(
            flight_manager.drone
        )

        self.mission_manager = MissionManager(
            flight_manager,
            mission
        )

        self.mission_manager.attach_state_machine(
            self.state_machine
        )

        self.executor = MissionExecutor(
            flight_manager,
            self.mission_manager
        )

        self.failsafe = FailsafeManager(
            flight_manager,
            self.battery,
            self.health,
            self.logger
        )

    async def start(self):

        self.logger.mission_started()

        try:

            await self.executor.execute()

            self.logger.mission_completed()

        except Exception as e:

            self.logger.log_error(str(e))

            await self.failsafe.execute()

            raise

        finally:

            self.recorder.close()

    async def health_report(self):

        await self.health.print_health()

    async def battery_report(self):

        await self.battery.print_status()

    def current_state(self):

        return self.state_machine.get_state()

    def log(self, message):

        self.logger.log(message)
