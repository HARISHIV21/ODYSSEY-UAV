#!/bin/bash

set -e

PROJECT_DIR="$HOME/UAV_Project"

echo "=================================="
echo "       ODYSSEY UAV LAUNCH"
echo "=================================="

# Locate PX4
PX4_DIR=$(find "$HOME" -maxdepth 6 -type d -name "PX4-Autopilot" 2>/dev/null | head -n 1)

if [ -z "$PX4_DIR" ]; then
    echo "ERROR: PX4-Autopilot directory not found."
    exit 1
fi

echo "[1/3] PX4 found: $PX4_DIR"

# Activate ODYSSEY environment
cd "$PROJECT_DIR"
source venv/bin/activate

# Start PX4 SITL with Gazebo
echo "[2/3] Starting PX4 SITL..."
cd "$PX4_DIR"
make px4_sitl gz_x500 > "$PROJECT_DIR/px4_sitl.log" 2>&1 &

PX4_PID=$!
echo "PX4 process started: $PX4_PID"

# Allow simulator time to initialize
sleep 20

# Launch ODYSSEY
echo "[3/3] Starting ODYSSEY..."
cd "$PROJECT_DIR"
python app.py
