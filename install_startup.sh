#!/bin/bash
# Install PDF Monitor as a Launch Agent (runs on startup)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_FILE="$SCRIPT_DIR/com.kevinreed.pdfmonitor.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
TARGET_PLIST="$LAUNCH_AGENTS_DIR/com.kevinreed.pdfmonitor.plist"

# Update plist with actual script path
sed "s|/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app|$SCRIPT_DIR|g" "$PLIST_FILE" > "$TARGET_PLIST"

# Load the launch agent
launchctl load "$TARGET_PLIST" 2>/dev/null || launchctl load -w "$TARGET_PLIST"

echo "✅ PDF Monitor installed as startup app"
echo "   It will automatically start when you log in"
echo ""
echo "To uninstall, run:"
echo "  launchctl unload $TARGET_PLIST"
echo "  rm $TARGET_PLIST"

