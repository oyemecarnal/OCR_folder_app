#!/bin/bash
# Create native macOS widget app bundle

cd "$(dirname "$0")"

APP_NAME="PDFMonitorWidget"
APP_DIR="${APP_NAME}.app"
CONTENTS_DIR="${APP_DIR}/Contents"
MACOS_DIR="${CONTENTS_DIR}/MacOS"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

echo "🔨 Creating Native macOS Widget App..."
echo ""

# Clean up old app
rm -rf "${APP_DIR}"

# Create directory structure
mkdir -p "${MACOS_DIR}"
mkdir -p "${RESOURCES_DIR}"

# Copy Python script
cp macos_widget_native.py "${MACOS_DIR}/${APP_NAME}.py"

# Create launcher script
cat > "${MACOS_DIR}/${APP_NAME}" <<'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 "${APP_NAME}.py"
EOF

chmod +x "${MACOS_DIR}/${APP_NAME}"
chmod +x "${MACOS_DIR}/${APP_NAME}.py"

# Create Info.plist
cat > "${CONTENTS_DIR}/Info.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>${APP_NAME}</string>
    <key>CFBundleIdentifier</key>
    <string>com.pdfmonitor.widget</string>
    <key>CFBundleName</key>
    <string>${APP_NAME}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>11.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <false/>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
</dict>
</plist>
EOF

echo "✅ Created ${APP_DIR}"
echo ""
echo "📱 To use:"
echo "   1. Make sure control server is running: ./start_ios_widget_server.sh"
echo "   2. Double-click ${APP_DIR}"
echo "   3. Native macOS widget window will appear!"
echo ""
echo "✨ Features:"
echo "   - Native macOS interface"
echo "   - Auto-refreshes every 10 seconds"
echo "   - Real-time status and statistics"
echo "   - One-click control buttons"
echo ""
echo "💡 Tips:"
echo "   - Add to Dock for quick access"
echo "   - Set as Login Item to auto-start"
echo "   - Resize window if needed (currently 350x500)"

