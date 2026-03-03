#!/bin/bash
# Launch PDF Monitor in menu bar with proper GUI context
cd "$(dirname "$0")"

# Use osascript to launch in GUI context
osascript <<'APPLESCRIPT'
tell application "System Events"
    set appPath to POSIX file "/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app"
    do shell script "cd " & quoted form of POSIX path of appPath & " && python3 pdf_monitor_app.py" without altering line endings
end tell
APPLESCRIPT

