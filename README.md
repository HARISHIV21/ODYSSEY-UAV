# ODYSSEY UAV

### Software-Defined Autonomous UAV Navigation & Mission Computer

ODYSSEY UAV is a modular autonomous unmanned aerial vehicle software platform developed around **PX4 SITL, Gazebo and MAVSDK-Python**.

The project implements a software-based UAV mission computer capable of vehicle connection, health verification, autonomous takeoff, offboard flight, waypoint navigation, mission-state management, telemetry acquisition, flight-data recording, failsafe handling and autonomous landing.

The complete system can be developed and validated without physical UAV hardware using Software-in-the-Loop simulation.

---

## System Architecture

```text
                     +----------------------+
                     |      Mission JSON    |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |    Mission Loader    |
                     +----------+-----------+
                                |
                                v
+----------------------------------------------------------+
|                    MISSION COMPUTER                      |
|                                                          |
|  +--------------+       +-----------------------------+  |
|  | State Machine|<----->|       Mission Manager       |  |
|  +--------------+       +--------------+--------------+  |
|                                        |                 |
|  +--------------+                      v                 |
|  |Health Monitor|              +---------------+         |
|  +--------------+              |Mission Executor|        |
|                                +-------+-------+         |
|  +--------------+                      |                 |
|  |Battery Monitor|                     v                 |
|  +--------------+              +---------------+         |
|                                |Flight Manager |         |
|  +--------------+              +-------+-------+         |
|  |Failsafe Mgr. |                      |                 |
|  +--------------+                      |                 |
|                                        |                 |
|  +--------------+     +----------------+---------------+ |
|  |Flight Recorder|    |                                | |
|  +--------------+     v                                v |
|                 +-------------+                +----------+
|                 | Navigation  |                | Offboard |
|                 |   Engine    |                |Controller|
|                 +-------------+                +----------+
+----------------------------------------------------------+
                         |
                         v
                  +-------------+
                  |   MAVSDK    |
                  +------+------+
                         |
                         v
                  +-------------+
                  |     PX4     |
                  |    SITL     |
                  +------+------+
                         |
                         v
                  +-------------+
                  |   Gazebo    |
                  | x500 Model  |
                  +-------------+
```

---

## Core Capabilities

- Autonomous mission execution
- PX4 vehicle connection through MAVSDK
- Pre-flight health verification
- Autonomous arming and takeoff
- Offboard position control
- NED waypoint navigation
- Real-time waypoint-distance calculation
- Waypoint arrival detection
- Mission progress tracking
- Mission state-machine architecture
- Battery monitoring
- Vehicle health monitoring
- Telemetry acquisition
- CSV flight-data recording
- Automatic mission reporting
- Failsafe landing logic
- Autonomous landing and disarming
- PX4/Gazebo Software-in-the-Loop validation

---

## Mission State Machine

ODYSSEY executes missions through deterministic mission states:

```text
INITIALIZE
    |
    v
CONNECT
    |
    v
WAIT_FOR_HEALTH
    |
    v
ARM
    |
    v
TAKEOFF
    |
    v
START_OFFBOARD
    |
    v
MISSION
    |
    v
WAYPOINT
    |
    +----> WAYPOINT
    |        ...
    |
    v
LAND
    |
    v
DISARM
    |
    v
COMPLETE
```

Failure conditions can transition execution into the failsafe handling path.

---

## Navigation

The navigation subsystem operates using the local **North-East-Down (NED)** coordinate frame.

For each mission waypoint, ODYSSEY calculates:

- 3D distance
- horizontal distance
- vertical distance
- waypoint arrival status

A waypoint is marked complete once the vehicle enters the configured position tolerance.

Example mission:

```text
WP1 -> N:5  E:0  D:-10
WP2 -> N:5  E:5  D:-10
WP3 -> N:0  E:5  D:-10
WP4 -> N:0  E:0  D:-10
```

This produces a square autonomous flight trajectory at approximately 10 m altitude.

---

## Mission Progress

During execution the mission computer reports mission completion status.

Example:

```text
========== MISSION PROGRESS ==========
Completed : 3/4
Remaining : 1
Progress  : 75.0%
======================================
```

---

## Flight Data Recorder

ODYSSEY records flight telemetry into timestamped CSV files.

Recorded parameters include:

```text
Time
North
East
Down
Battery(%)
FlightMode
```

Runtime flight logs are stored locally under:

```text
Logs/
```

Generated runtime logs are intentionally excluded from version control.

---

## Failsafe Architecture

The mission computer contains a dedicated failsafe manager.

Monitored conditions include:

- battery state
- vehicle health
- mission execution exceptions

The failsafe path attempts to:

```text
Detect Failure
     |
     v
Stop Offboard Control
     |
     v
Command Landing
     |
     v
Disarm Vehicle
     |
     v
Safe State
```

---

## Project Structure

```text
UAV_Project/
|
+-- Communication/
+-- Config/
+-- Control/
+-- Core/
+-- Data/
+-- Documentation/
+-- Logs/
+-- MissionComputer/
|   +-- battery_monitor.py
|   +-- failsafe_manager.py
|   +-- flight_manager.py
|   +-- flight_recorder.py
|   +-- health_monitor.py
|   +-- logger.py
|   +-- mission_computer.py
|   +-- mission_executor.py
|   +-- mission_manager.py
|   +-- offboard_controller.py
|   +-- state_machine.py
|   +-- telemetry_manager.py
|
+-- Navigation/
|   +-- distance.py
|   +-- mission_loader.py
|   +-- mission_planner.py
|   +-- navigation_engine.py
|   +-- trajectory.py
|   +-- waypoint_tracker.py
|
+-- Sensors/
+-- Telemetry/
+-- Utils/
|   +-- mission_report.py
|
+-- Missions/
+-- app.py
+-- requirements.txt
+-- LICENSE
+-- README.md
```

---

## Technology Stack

- Python 3
- MAVSDK-Python
- PX4 Autopilot
- PX4 SITL
- Gazebo
- AsyncIO
- Git / GitHub
- Ubuntu / WSL

---

## Running ODYSSEY

### Terminal 1 — Start PX4 SITL

```bash
cd ~/Projects/PX4-Autopilot
HEADLESS=1 make px4_sitl gz_x500
```

Wait until PX4 reaches:

```text
pxh>
```

### Terminal 2 — Start the Mission Computer

```bash
cd ~/UAV_Project
source venv/bin/activate
python app.py
```

---

## Example Successful Mission

A successful ODYSSEY mission performs:

```text
PX4 Connection
      |
Vehicle Health Check
      |
     ARM
      |
   TAKEOFF
      |
Start Offboard Control
      |
Waypoint Navigation
      |
Mission Progress = 100%
      |
     LAND
      |
    DISARM
      |
MISSION COMPLETE
```

---

## Simulation Validation

The system has been validated in PX4/Gazebo SITL using an x500 multicopter simulation.

Validated functionality includes:

- PX4 connection
- health verification
- autonomous arming
- autonomous takeoff
- offboard control
- four-waypoint square navigation
- waypoint arrival detection
- 100% mission progress
- telemetry recording
- autonomous landing
- disarming
- mission completion

---

## Design Philosophy

ODYSSEY separates mission-level autonomy from low-level flight control.

PX4 handles vehicle stabilization and low-level flight control while ODYSSEY operates as the higher-level mission computer responsible for mission sequencing, navigation decisions, monitoring, telemetry and safety management.

This modular separation allows additional autonomy functions to be integrated without redesigning the complete flight-control stack.

---

## Future Extensions

Potential future development includes:

- obstacle avoidance
- path replanning
- computer-vision perception
- GNSS-denied navigation
- sensor fusion
- geofencing
- return-to-home logic
- ROS 2 integration
- multi-UAV coordination
- hardware flight-computer deployment

---

## License

See `LICENSE` for licensing information.
