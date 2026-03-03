#!/bin/bash
# Script to check menu bar visibility and help diagnose issues

echo "=== PDF Monitor Menu Bar Diagnostic ==="
echo ""

# Check if app is running
echo "1. Checking if app is running..."
if ps aux | grep -i "pdf_monitor_app" | grep -v grep > /dev/null; then
    echo "   ✓ App IS running"
    ps aux | grep -i "pdf_monitor_app" | grep -v grep | head -1
else
    echo "   ✗ App is NOT running"
    echo "   Start it with: python3 pdf_monitor_app.py"
    exit 1
fi

echo ""
echo "2. Checking menu bar items..."
echo "   Looking for 'PDF Monitor' or '📄 PDF Monitor' in menu bar..."

# Try to check menu bar programmatically
osascript <<EOF 2>/dev/null
tell application "System Events"
    try
        set menuBarItems to name of every menu bar item of menu bar 1
        repeat with itemName in menuBarItems
            if itemName contains "PDF Monitor" or itemName contains "📄" then
                return "Found: " & itemName
            end if
        end repeat
        return "Not found in visible menu bar items"
    on error
        return "Could not check menu bar (permission issue?)"
    end try
end tell
EOF

echo ""
echo "3. Troubleshooting steps:"
echo "   a) Look for '📄 PDF Monitor' in top-right menu bar"
echo "   b) Check overflow area (>> icon on far right)"
echo "   c) Try: killall SystemUIServer (refreshes menu bar)"
echo "   d) Free up menu bar space (System Settings → Control Center)"
echo ""
echo "4. Alternative access methods:"
echo "   - Web interface: python3 pdf_monitor_web.py"
echo "   - CLI tools: python3 manage_folders.py list"
echo "   - Check logs: tail -f logs/pdf_monitor_app.log"
echo ""

