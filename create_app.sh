#!/bin/bash
# Create a proper macOS app bundle that can be double-clicked

APP_DIR="$HOME/Applications/PDFMonitor.app"
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Creating macOS app bundle..."

# Remove old app if exists
rm -rf "$APP_DIR"

# Create app structure
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

# Create Info.plist
cat > "$APP_DIR/Contents/Info.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>PDFMonitor</string>
    <key>CFBundleIdentifier</key>
    <string>com.pdfmonitor.app</string>
    <key>CFBundleName</key>
    <string>PDF Monitor</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>LSUIElement</key>
    <true/>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

# Create executable with proper path substitution
cat > "$APP_DIR/Contents/MacOS/PDFMonitor" <<EOF
#!/bin/bash
cd "$SOURCE_DIR"
exec python3 pdf_monitor_app.py
EOF

chmod +x "$APP_DIR/Contents/MacOS/PDFMonitor"

echo "✅ App bundle created at: $APP_DIR"
echo "You can now double-click it to launch!"

