#!/bin/bash
# Robust launcher for PDF Monitor menu bar app
# This script ensures proper environment and visibility

cd "$(dirname "$0")"

echo "Starting PDF Monitor menu bar app..."
echo "This may take a few seconds to appear in your menu bar"
echo ""

# Kill any existing instances
pkill -f "pdf_monitor_app.py" 2>/dev/null
sleep 1

# Set environment variables for better compatibility
export PYTHONUNBUFFERED=1

# Run the app with output visible for debugging
python3 pdf_monitor_app.py 2>&1 | tee -a logs/menu_bar_launch.log

