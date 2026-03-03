#!/bin/bash
# Create macOS Widget App from Swift file

cd "$(dirname "$0")"

echo "🔨 Creating macOS Widget App..."
echo ""

# Check if Swift is available
if ! command -v swift &> /dev/null; then
    echo "❌ Swift is not installed"
    echo "   Install Xcode from the App Store"
    exit 1
fi

# Create a simple macOS app bundle structure
APP_NAME="PDFMonitorWidget"
APP_DIR="${APP_NAME}.app"
CONTENTS_DIR="${APP_DIR}/Contents"
MACOS_DIR="${CONTENTS_DIR}/MacOS"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

# Clean up old app if exists
rm -rf "${APP_DIR}"

# Create directory structure
mkdir -p "${MACOS_DIR}"
mkdir -p "${RESOURCES_DIR}"

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
    <string>12.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>
EOF

# Compile Swift file (if we have a proper Swift project)
# For now, create a simple launcher that opens the web interface
cat > "${MACOS_DIR}/${APP_NAME}" <<'EOF'
#!/bin/bash
# Launch PDF Monitor Widget
open "http://localhost:5002"
EOF

chmod +x "${MACOS_DIR}/${APP_NAME}"

echo "✅ Created ${APP_DIR}"
echo ""
echo "📱 To use:"
echo "   1. Double-click ${APP_DIR}"
echo "   2. It will open the widget in your default browser"
echo ""
echo "💡 For a native macOS widget, you'll need to:"
echo "   1. Open Xcode"
echo "   2. Create a new macOS App project"
echo "   3. Use the SwiftUI code in macos_widget_app.swift"
echo "   4. Build and run"
echo ""
echo "📖 See MACOS_WIDGET_SETUP.md for detailed instructions"

