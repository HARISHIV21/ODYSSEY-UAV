import csv
import os
from datetime import datetime


class FlightRecorder:

    def __init__(self):

        os.makedirs("Logs", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.filename = f"Logs/flight_data_{timestamp}.csv"

        self.file = open(self.filename, "w", newline="")

        self.writer = csv.writer(self.file)

        self.writer.writerow([
            "Time",
            "North",
            "East",
            "Down",
            "Battery(%)",
            "FlightMode"
        ])

        self.closed = False

        print(f"[RECORDER] Logging to {self.filename}")

    def record(
        self,
        elapsed_time,
        north,
        east,
        down,
        battery,
        mode
    ):

        if self.closed:
            return

        self.writer.writerow([
            f"{elapsed_time:.2f}",
            f"{north:.2f}",
            f"{east:.2f}",
            f"{down:.2f}",
            f"{battery:.1f}",
            mode
        ])

        self.file.flush()

    def close(self):

        if self.closed:
            return

        self.closed = True

        self.file.close()

        print("[RECORDER] Flight log saved")
