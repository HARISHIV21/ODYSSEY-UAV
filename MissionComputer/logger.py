from pathlib import Path
from datetime import datetime


class MissionLogger:

    def __init__(self, log_directory="Logs"):

        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.log_file = self.log_directory / f"mission_{timestamp}.log"

        with open(self.log_file, "w") as f:
            f.write("=" * 60 + "\n")
            f.write("ODYSSEY UAV MISSION LOG\n")
            f.write("=" * 60 + "\n\n")

    def log(self, message):

        timestamp = datetime.now().strftime("%H:%M:%S")

        line = f"[{timestamp}] {message}"

        print(line)

        with open(self.log_file, "a") as f:
            f.write(line + "\n")

    def separator(self):

        with open(self.log_file, "a") as f:
            f.write("-" * 60 + "\n")

    def log_state(self, state):

        self.log(f"STATE -> {state}")

    def log_waypoint(self, index, total):

        self.log(f"Waypoint {index}/{total}")

    def log_error(self, error):

        self.log(f"ERROR : {error}")

    def log_warning(self, warning):

        self.log(f"WARNING : {warning}")

    def mission_started(self):

        self.separator()
        self.log("MISSION STARTED")

    def mission_completed(self):

        self.log("MISSION COMPLETED")
        self.separator()

    def get_log_file(self):

        return str(self.log_file)
