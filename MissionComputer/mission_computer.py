import asyncio
import time

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

        # Logging
        self.logger = MissionLogger()
        self.recorder = FlightRecorder()

        # State machine
        self.state_machine = StateMachine()

        # Vehicle monitoring
        self.battery = BatteryMonitor(
            flight_manager.drone
        )

        self.health = HealthMonitor(
            flight_manager.drone
        )

        # Mission manager
        self.mission_manager = MissionManager(
            flight_manager,
            mission
        )

        self.mission_manager.attach_state_machine(
            self.state_machine
        )

        # Mission executor
        self.executor = MissionExecutor(
            flight_manager,
            self.mission_manager
        )

        # Failsafe
        self.failsafe = FailsafeManager(
            flight_manager,
            self.battery,
            self.health,
            self.logger
        )

        # Flight recorder control
        self.recording = False
        self.recording_task = None

    async def flight_recording_loop(self):

        start_time = time.monotonic()

        print("[RECORDER] Waiting for telemetry...")

        # -------------------------------------------------
        # WAIT FOR MAVSDK TELEMETRY
        # -------------------------------------------------

        while self.recording:

            try:

                await self.flight_manager.telemetry.update()

                if self.flight_manager.telemetry.ready():
                    break

            except asyncio.CancelledError:

                return

            except Exception:

                # PX4 may still be completing connection
                await asyncio.sleep(0.5)

        if not self.recording:
            return

        print("[RECORDER] Live recording started")

        # -------------------------------------------------
        # RECORD FLIGHT DATA
        # -------------------------------------------------

        while self.recording:

            try:

                await self.flight_manager.telemetry.update()

                snapshot = (
                    self.flight_manager.telemetry.get_snapshot()
                )

                elapsed_time = (
                    time.monotonic() - start_time
                )

                try:

                    state = self.state_machine.get_state()

                    state_name = str(state)

                except Exception:

                    state_name = snapshot["flight_mode"]

                self.recorder.record(
                    elapsed_time,
                    snapshot["north"],
                    snapshot["east"],
                    snapshot["down"],
                    snapshot["battery"],
                    state_name
                )

            except asyncio.CancelledError:

                break

            except Exception as e:

                print(
                    f"[RECORDER] Telemetry warning: {e}"
                )

            await asyncio.sleep(1)

        print("[RECORDER] Live recording stopped")

    async def start(self):

        self.logger.mission_started()

        # Start recorder background task
        self.recording = True

        self.recording_task = asyncio.create_task(
            self.flight_recording_loop()
        )

        try:

            await self.executor.execute()

            self.logger.mission_completed()

        except Exception as e:

            self.logger.log_error(str(e))

            await self.failsafe.execute()

            raise

        finally:

            # Stop recorder
            self.recording = False

            if self.recording_task:

                self.recording_task.cancel()

                try:

                    await self.recording_task

                except asyncio.CancelledError:

                    pass

            self.recorder.close()

    async def health_report(self):

        await self.health.print_health()

    async def battery_report(self):

        await self.battery.print_status()

    def current_state(self):

        return self.state_machine.get_state()

    def log(self, message):

        self.logger.log(message)
