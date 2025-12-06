#!/bin/bash
# Launch PDF Monitor menu bar app
cd "$(dirname "$0")"
osascript -e 'tell application "Terminal" to do script "cd \"'"$(pwd)"'\" && python3 pdf_monitor_app.py"' || python3 pdf_monitor_app.py &



