#!/bin/bash
# Create desktop launchers for PDF Monitor

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DESKTOP="$HOME/Desktop"

echo "Creating PDF Monitor launchers on Desktop..."

# Copy launcher apps to Desktop
cp -r "$SCRIPT_DIR/PDFMonitorLauncher.app" "$DESKTOP/" 2>/dev/null
cp -r "$SCRIPT_DIR/PDFMonitorStop.app" "$DESKTOP/" 2>/dev/null

# Also copy to Applications for easy access
mkdir -p "$HOME/Applications"
cp -r "$SCRIPT_DIR/PDFMonitorLauncher.app" "$HOME/Applications/" 2>/dev/null
cp -r "$SCRIPT_DIR/PDFMonitorStop.app" "$HOME/Applications/" 2>/dev/null

echo "✅ Launchers created!"
echo ""
echo "On Desktop:"
echo "  - PDFMonitorLauncher.app (double-click to start)"
echo "  - PDFMonitorStop.app (double-click to stop)"
echo ""
echo "In Applications:"
echo "  - PDFMonitorLauncher.app"
echo "  - PDFMonitorStop.app"
echo ""
echo "You can drag these to your Dock for quick access!"

