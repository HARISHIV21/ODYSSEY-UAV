#!/usr/bin/env bash

set -e

capture_screen() {
    local output="$1"
    local winpath

    mkdir -p "$(dirname "$output")"
    winpath=$(wslpath -w "$(realpath -m "$output")")

    echo
    echo "======================================"
    echo "Screenshot: $(basename "$output")"
    echo "======================================"
    echo "1. Bring the correct application to the foreground."
    read -rp "2. Press Enter here when ready: "
    sleep 3

    powershell.exe -NoProfile -Command "
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        \$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        \$bitmap = New-Object System.Drawing.Bitmap(\$bounds.Width,\$bounds.Height)
        \$graphics = [System.Drawing.Graphics]::FromImage(\$bitmap)
        \$graphics.CopyFromScreen(\$bounds.Location,[System.Drawing.Point]::Empty,\$bounds.Size)
        \$bitmap.Save('$winpath',[System.Drawing.Imaging.ImageFormat]::Png)
        \$graphics.Dispose()
        \$bitmap.Dispose()
    "

    test -s "$output"
    echo "Saved: $output"
}

E="$HOME/UAV_Project/Documentation/Evidence"

capture_screen "$E/01_Architecture/windows_architecture.png"
capture_screen "$E/02_Mission/windows_mission.png"
capture_screen "$E/03_Navigation/windows_navigation.png"
capture_screen "$E/04_Flight_Control/windows_flight_control.png"
capture_screen "$E/05_Safety/windows_safety.png"
capture_screen "$E/06_Telemetry/windows_telemetry.png"
capture_screen "$E/07_Recording/windows_recording.png"
capture_screen "$E/08_Testing/windows_testing.png"
capture_screen "$E/09_SITL/windows_sitl.png"
capture_screen "$E/10_Analysis/windows_analysis.png"

echo
echo "Screenshot capture sequence completed."
