# macOS Widget Setup Guide

## 🎯 Overview

There are several ways to create a macOS widget for PDF Monitor:

1. **Simple Browser Widget** (Easiest) - Opens widget in browser
2. **Native SwiftUI App** (Best) - True native macOS widget
3. **Menu Bar Widget** (Alternative) - Status in menu bar

## 🚀 Option 1: Simple Browser Widget (Recommended for Quick Setup)

This creates a macOS app that opens the widget in your browser.

### Setup:

```bash
chmod +x create_macos_widget.sh
./create_macos_widget.sh
```

This creates `PDFMonitorWidget.app` that you can:
- Double-click to open the widget
- Add to Dock
- Add to Applications folder

### Usage:
1. Make sure control server is running: `./start_ios_widget_server.sh`
2. Double-click `PDFMonitorWidget.app`
3. Widget opens in your browser

## 🎨 Option 2: Native SwiftUI Widget (Best Experience)

For a true native macOS widget, you need Xcode.

### Requirements:
- Xcode (from App Store)
- macOS 12.0 or later

### Steps:

1. **Open Xcode**
   - Create New Project
   - Choose "macOS" → "App"
   - Name it "PDFMonitorWidget"
   - Language: Swift
   - Interface: SwiftUI

2. **Replace the ContentView.swift** with the code from `macos_widget_app.swift`

3. **Build and Run**
   - Press Cmd+R to build
   - The widget window will appear

4. **Customize Window**
   - The window is set to 350x450 pixels
   - You can resize or make it floating
   - Add to Dock for quick access

### Features:
- ✅ Native macOS interface
- ✅ Auto-refreshes every 10 seconds
- ✅ Real-time status updates
- ✅ One-click control buttons
- ✅ Statistics display

## 📊 Option 3: Menu Bar Widget (Status Only)

You can also create a simple menu bar status indicator.

### Create Menu Bar Status App:

```bash
# This would require a separate Swift app
# See menu_bar_status_app.swift (to be created)
```

## 🔧 Configuration

### Change Widget Size:
In `macos_widget_app.swift`, modify:
```swift
.frame(width: 350, height: 450)
```

### Change Refresh Rate:
Modify the timer interval:
```swift
let timer = Timer.publish(every: 10, on: .main, in: .common).autoconnect()
// Change 10 to desired seconds
```

### Change Server URL:
If server runs on different port:
```swift
URL(string: "http://localhost:5002/api/status")
// Change port number
```

## 🎯 Quick Start (Native Widget)

1. **Install Xcode** (if not installed)
   ```bash
   # Open App Store and search "Xcode"
   ```

2. **Create Project**
   - Open Xcode
   - File → New → Project
   - macOS → App
   - Use SwiftUI

3. **Copy Code**
   - Copy contents of `macos_widget_app.swift`
   - Replace your ContentView.swift

4. **Run**
   - Press Cmd+R
   - Widget appears!

## 📱 Widget Features

- **Status Display** - Green circle = ON, Red = OFF
- **Statistics** - Processed files and errors
- **Control Buttons** - Toggle, Turn ON/OFF
- **Auto-Refresh** - Updates every 10 seconds
- **Native Design** - Uses macOS system colors

## 🐛 Troubleshooting

### Widget won't connect:
- Make sure control server is running: `./start_ios_widget_server.sh`
- Check server is on port 5002
- Try: `http://localhost:5002/api/status` in browser

### Xcode errors:
- Make sure you're using macOS 12.0+
- Update Xcode to latest version
- Check Swift version: `swift --version`

### Widget doesn't update:
- Check network connection
- Verify server is running
- Check firewall settings

## 💡 Tips

1. **Add to Dock** - Drag widget app to Dock for quick access
2. **Set as Login Item** - Auto-start widget on login
3. **Multiple Monitors** - Widget works on all displays
4. **Keyboard Shortcuts** - Can add global shortcuts (advanced)

## 🎨 Customization

### Change Colors:
```swift
var statusColor: Color {
    status == "on" ? .green : .red
}
// Change to any SwiftUI Color
```

### Change Layout:
Modify the VStack/HStack structure in the body

### Add More Stats:
Add more StatBox views

## 📚 Next Steps

1. ✅ Choose your preferred option
2. ✅ Follow setup instructions
3. ✅ Customize to your liking
4. ✅ Enjoy your macOS widget!

For the simplest setup, use **Option 1** (Browser Widget).
For the best experience, use **Option 2** (Native SwiftUI).

