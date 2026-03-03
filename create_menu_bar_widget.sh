#!/bin/bash
# Create Menu Bar Widget App

cd "$(dirname "$0")"

APP_NAME="PDFMonitorMenuBar"
APP_DIR="${APP_NAME}.app"
CONTENTS_DIR="${APP_DIR}/Contents"
MACOS_DIR="${CONTENTS_DIR}/MacOS"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

echo "🔨 Creating Menu Bar Widget..."
echo ""

# Clean up old app
rm -rf "${APP_DIR}"

# Create directory structure
mkdir -p "${MACOS_DIR}"
mkdir -p "${RESOURCES_DIR}"

# Copy Python script
cp menu_bar_widget.py "${MACOS_DIR}/${APP_NAME}.py"

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
    <string>com.pdfmonitor.menubar</string>
    <key>CFBundleName</key>
    <string>${APP_NAME}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>11.0</string>
    <key>LSUIElement</key>
    <true/>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

echo "✅ Created ${APP_DIR}"
echo ""
echo "📱 Features:"
echo "   ✓ Always visible in menu bar (📄 icon)"
echo "   ✓ Color indicator (🟢 = ON, 🔴 = OFF)"
echo "   ✓ Click to see status and controls"
echo "   ✓ Quick access to widget window"
echo ""
echo "🚀 To use:"
echo "   1. Double-click ${APP_DIR}"
echo "   2. Look for '📄' in menu bar (top right)"
echo "   3. Click it to see menu and controls"

