#!/bin/bash
cd "/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app"

# Show notification that app is starting
osascript -e 'display notification "Starting PDF Monitor..." with title "PDF Monitor"'

# Run the app
python3 pdf_monitor_app.py &
APP_PID=$!

# Wait a moment and check if it's running
sleep 2
if ps -p $APP_PID > /dev/null; then
    osascript -e 'display notification "PDF Monitor is running! Look for it in your menu bar (top right)." with title "PDF Monitor"'
    echo "✅ PDF Monitor is running (PID: $APP_PID)"
    echo "📋 Look for 'PDF Monitor' in your menu bar (top right)"
    echo "   If you don't see it, check the overflow menu (arrow icon)"
else
    osascript -e 'display notification "PDF Monitor failed to start. Check Terminal for errors." with title "PDF Monitor"'
    echo "❌ PDF Monitor failed to start"
fi
