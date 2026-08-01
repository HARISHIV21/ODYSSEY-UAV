import csv
import glob
import os

import matplotlib.pyplot as plt


LOG_DIRECTORY = "Logs"
OUTPUT_DIRECTORY = "Images"
OUTPUT_FILE = "07_trajectory_validation.png"


def find_latest_log():
    """Return the newest ODYSSEY flight recorder CSV."""

    pattern = os.path.join(
        LOG_DIRECTORY,
        "flight_data_*.csv"
    )

    files = glob.glob(pattern)

    if not files:
        raise FileNotFoundError(
            "No flight_data_*.csv files found in Logs/"
        )

    return max(files, key=os.path.getmtime)


def load_trajectory(filename):
    """Load North/East position data from flight recorder."""

    north = []
    east = []

    with open(filename, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            try:
                north_value = float(row["North"])
                east_value = float(row["East"])

                north.append(north_value)
                east.append(east_value)

            except (ValueError, KeyError):
                continue

    if not north:
        raise RuntimeError(
            "No valid North/East trajectory data found."
        )

    return north, east


def calculate_horizontal_error(north, east):
    """Calculate final horizontal distance from origin."""

    final_north = north[-1]
    final_east = east[-1]

    return (
        final_north ** 2
        + final_east ** 2
    ) ** 0.5


def create_plot(north, east, source_file):

    # -------------------------------------------------
    # Commanded ODYSSEY square mission
    #
    # Start -> WP1 -> WP2 -> WP3 -> WP4
    #
    # N:0 E:0
    # N:5 E:0
    # N:5 E:5
    # N:0 E:5
    # N:0 E:0
    # -------------------------------------------------

    commanded_north = [
        0,
        5,
        5,
        0,
        0,
    ]

    commanded_east = [
        0,
        0,
        5,
        5,
        0,
    ]

    figure, axis = plt.subplots(
        figsize=(9, 8)
    )

    # Commanded mission path
    axis.plot(
        commanded_east,
        commanded_north,
        "--",
        linewidth=2.2,
        label="Commanded Trajectory",
    )

    # Actual PX4 trajectory
    axis.plot(
        east,
        north,
        "-o",
        linewidth=2.0,
        markersize=4,
        label="PX4 Actual Trajectory",
    )

    # Mission waypoints
    axis.scatter(
        commanded_east[1:],
        commanded_north[1:],
        s=80,
        marker="D",
        label="Mission Waypoints",
        zorder=5,
    )

    # Start position
    axis.scatter(
        east[0],
        north[0],
        s=120,
        marker="s",
        label="Start Position",
        zorder=6,
    )

    # Final recorded position
    axis.scatter(
        east[-1],
        north[-1],
        s=140,
        marker="X",
        label="Final Position",
        zorder=7,
    )

    # Waypoint labels
    waypoint_labels = [
        "WP1",
        "WP2",
        "WP3",
        "WP4",
    ]

    waypoint_positions = [
        (0, 5),
        (5, 5),
        (5, 0),
        (0, 0),
    ]

    for label, position in zip(
        waypoint_labels,
        waypoint_positions
    ):

        wp_east, wp_north = position

        axis.annotate(
            label,
            (wp_east, wp_north),
            xytext=(7, 7),
            textcoords="offset points",
            fontsize=9,
        )

    horizontal_error = calculate_horizontal_error(
        north,
        east
    )

    # Engineering information box
    information = (
        f"Samples: {len(north)}\n"
        f"Final N: {north[-1]:.2f} m\n"
        f"Final E: {east[-1]:.2f} m\n"
        f"Return Error: {horizontal_error:.2f} m"
    )

    axis.text(
        0.02,
        0.98,
        information,
        transform=axis.transAxes,
        verticalalignment="top",
        bbox={
            "boxstyle": "round",
            "alpha": 0.15,
        },
    )

    axis.set_title(
        "ODYSSEY UAV\n"
        "Autonomous Waypoint Navigation Validation",
        fontsize=15,
        pad=15,
    )

    axis.set_xlabel(
        "East Position (m)",
        fontsize=11,
    )

    axis.set_ylabel(
        "North Position (m)",
        fontsize=11,
    )

    axis.grid(
        True,
        linestyle="--",
        alpha=0.4,
    )

    axis.legend(
        loc="best",
        frameon=True,
    )

    axis.axis("equal")

    figure.text(
        0.5,
        0.015,
        "PX4 SITL + Gazebo | MAVSDK Offboard Control | Local NED Frame",
        ha="center",
        fontsize=9,
    )

    os.makedirs(
        OUTPUT_DIRECTORY,
        exist_ok=True
    )

    output_path = os.path.join(
        OUTPUT_DIRECTORY,
        OUTPUT_FILE
    )

    plt.tight_layout(
        rect=[0, 0.04, 1, 1]
    )

    figure.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    print()
    print("========================================")
    print(" ODYSSEY TRAJECTORY VALIDATION")
    print("========================================")
    print(f"Source Log       : {source_file}")
    print(f"Samples          : {len(north)}")
    print(
        f"Final Position   : "
        f"N={north[-1]:.2f} m, "
        f"E={east[-1]:.2f} m"
    )
    print(
        f"Return Error     : "
        f"{horizontal_error:.2f} m"
    )
    print(f"Output           : {output_path}")
    print("========================================")


def main():

    source_file = find_latest_log()

    north, east = load_trajectory(
        source_file
    )

    create_plot(
        north,
        east,
        source_file
    )


if __name__ == "__main__":
    main()
