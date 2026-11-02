import asyncio
from MissionComputer.state_machine import MissionState


class MissionExecutor:

    def __init__(self, flight_manager, mission_manager):

        self.fm = flight_manager
        self.mm = mission_manager

    async def execute(self):

        print("\n==============================")
        print("MISSION EXECUTOR")
        print("==============================")

        try:

            await self.mm.run()

        except asyncio.CancelledError:

            print("[EXECUTOR] Mission Cancelled")
            raise

        except Exception as e:

            print(f"[EXECUTOR] ERROR : {e}")

            if self.mm.state_machine:
                self.mm.state_machine.set_state(MissionState.FAILSAFE)

            raise

        finally:

            print("\n==============================")
            print("EXECUTOR FINISHED")
            print("==============================")
