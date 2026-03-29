#!/bin/bash

DEVICE="/dev/video2"  # Change if using a different device

echo "Reading controls from: $DEVICE"
echo "---------------------------------------------------------"

# List all controls with current and default values
v4l2-ctl -d "$DEVICE" --list-ctrls --all | while read -r line; do
    # Match lines like:              brightness (int)    : min=-64 max=64 step=1 default=0 value=0
    if [[ "$line" =~ ^[[:space:]]*([a-zA-Z0-9_-]+)[[:space:]]+\([^)]+\)[[:space:]]+.*default=([-0-9]+)[[:space:]]+value=([-0-9]+) ]]; then
        name="${BASH_REMATCH[1]}"
        default="${BASH_REMATCH[2]}"
        current="${BASH_REMATCH[3]}"

        echo "Control: $name | Current: $current | Default: $default"

        # Reset to default only if current != default
        if [[ "$current" != "$default" ]]; then
            echo "  → Resetting $name to $default"
            v4l2-ctl -d "$DEVICE" --set-ctrl "$name=$default" >/dev/null 2>&1
            if [[ $? -ne 0 ]]; then
                echo "  ⚠️ Failed to reset $name"
            fi
        fi
    fi
done

echo "---------------------------------------------------------"
echo "All camera controls reset to default (where applicable)."

