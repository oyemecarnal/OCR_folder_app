#!/bin/bash
# Get the app bundle directory
APP_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$APP_DIR"
export PYTHONUNBUFFERED=1
# Run the Python app - this ensures GUI context
exec /Library/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python pdf_monitor_app.py

