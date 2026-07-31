import csv
import glob
import os


class MissionReport:

    def __init__(self, log_directory="Logs"):

        self.log_directory = log_directory

    def latest_flight_log(self):

        files = glob.glob(
            os.path.join(
                self.log_directory,
                "flight_data_*.csv"
            )
        )

        if not files:
            return None

        return max(
            files,
            key=os.path.getmtime
        )

    def load_data(self, filename):

        data = []

        with open(
            filename,
            "r",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                try:

                    data.append({
                        "time": float(
                            row["Time"]
                        ),
                        "north": float(
                            row["North"]
                        ),
                        "east": float(
                            row["East"]
                        ),
                        "down": float(
                            row["Down"]
                        ),
                        "battery": float(
                            row["Battery(%)"]
                        ),
                        "mode": row[
                            "FlightMode"
                        ],
                    })

                except (
                    ValueError,
                    KeyError
                ):

                    continue

        return data

    def generate(self):

        filename = self.latest_flight_log()

        print("\n==============================")
        print("ODYSSEY POST-FLIGHT REPORT")
        print("==============================")

        if filename is None:

            print(
                "No flight recorder data found."
            )

            print("==============================")

            return

        data = self.load_data(
            filename
        )

        if not data:

            print(
                "Flight log contains no valid data."
            )

            print("==============================")

            return

        first = data[0]
        last = data[-1]

        duration = (
            last["time"] - first["time"]
        )

        if duration < 0:
            duration = 0.0

        max_altitude = max(
            -row["down"]
            for row in data
        )

        min_battery = min(
            row["battery"]
            for row in data
        )

        start_battery = first[
            "battery"
        ]

        end_battery = last[
            "battery"
        ]

        battery_used = (
            start_battery - end_battery
        )

        if battery_used < 0:
            battery_used = 0.0

        max_north = max(
            row["north"]
            for row in data
        )

        min_north = min(
            row["north"]
            for row in data
        )

        max_east = max(
            row["east"]
            for row in data
        )

        min_east = min(
            row["east"]
            for row in data
        )

        print(
            f"Flight Log       : {filename}"
        )

        print(
            f"Samples Recorded : {len(data)}"
        )

        print(
            f"Recorded Duration: {duration:.2f} s"
        )

        print(
            f"Maximum Altitude : {max_altitude:.2f} m"
        )

        print(
            f"North Range      : "
            f"{min_north:.2f} to "
            f"{max_north:.2f} m"
        )

        print(
            f"East Range       : "
            f"{min_east:.2f} to "
            f"{max_east:.2f} m"
        )

        print(
            f"Start Battery    : {start_battery:.1f}%"
        )

        print(
            f"End Battery      : {end_battery:.1f}%"
        )

        print(
            f"Minimum Battery  : {min_battery:.1f}%"
        )

        print(
            f"Battery Used     : {battery_used:.1f}%"
        )

        print(
            f"Final Position   : "
            f"N={last['north']:.2f}, "
            f"E={last['east']:.2f}, "
            f"D={last['down']:.2f}"
        )

        print(
            f"Final State      : {last['mode']}"
        )

        print("==============================")


if __name__ == "__main__":

    report = MissionReport()

    report.generate()
