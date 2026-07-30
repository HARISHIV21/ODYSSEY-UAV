from datetime import datetime
from pathlib import Path


class MissionLogger:

    def __init__(self):
        Path("../Logs").mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.file = open(
            f"../Logs/mission_{timestamp}.log",
            "w"
        )

    def log(self, message):

        line = (
            f"[{datetime.now().strftime('%H:%M:%S')}] "
            f"{message}"
        )

        print(line)

        self.file.write(line + "\n")
        self.file.flush()

    def close(self):
        self.file.close()
