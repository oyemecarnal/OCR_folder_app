#!/bin/bash
cd "$(dirname "$0")"
# Launch in GUI mode using osascript
osascript <<EOF
tell application "Terminal"
    do script "cd '$PWD' && python3 pdf_monitor_app.py"
end tell
EOF

