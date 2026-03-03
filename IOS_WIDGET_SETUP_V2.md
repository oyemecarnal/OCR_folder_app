# iOS Widget Setup - PDF Monitor Control

## 🎯 Overview

This guide shows you how to create an iOS widget to control your PDF Monitor app from your iPhone/iPad. The widget works like a native iOS app and can be added to your home screen.

## ✨ Features

- **Native iOS Widget** - Looks and feels like a real iOS app
- **Real-time Status** - Shows current monitor status
- **Statistics** - Displays processed files and errors
- **One-Tap Control** - Toggle monitor on/off with a tap
- **Auto-Refresh** - Updates every 10 seconds
- **Works Offline** - Caches status when Mac is sleeping

## 🚀 Quick Setup (5 minutes)

### Step 1: Start the Enhanced Control Server

On your Mac, run:

```bash
cd /Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app
python3 ocr_control_server_enhanced.py
```

**Or use the launcher script:**
```bash
./start_ios_widget_server.sh
```

The server will start on **port 5002** and display:
```
🌐 Web Widget: http://localhost:5002
📱 iOS Widget: Add to Home Screen from Safari
```

### Step 2: Find Your Mac's IP Address

On your Mac, run:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1
```

You'll get something like: `192.168.1.100`

### Step 3: Add Widget to iOS Home Screen

1. **On your iPhone/iPad**, open **Safari**
2. **Navigate to**: `http://YOUR_MAC_IP:5002`
   - Replace `YOUR_MAC_IP` with the IP from Step 2
   - Example: `http://192.168.1.100:5002`
3. **Wait for the widget to load** (you'll see a nice interface)
4. **Tap the Share button** (square with arrow) at the bottom
5. **Scroll down** and tap **"Add to Home Screen"**
6. **Customize the name** (e.g., "PDF Monitor")
7. **Tap "Add"**

### Step 4: Use Your Widget!

- **Tap the widget** on your home screen
- **See status** - Green = ON, Red = OFF
- **View statistics** - Processed files and errors
- **Toggle monitor** - Tap buttons to control

## 📱 Widget Features

### Status Display
- **Green indicator** = Monitor is ON
- **Red indicator** = Monitor is OFF
- **Real-time updates** every 10 seconds

### Statistics
- **Processed** - Total files processed
- **Errors** - Number of errors encountered

### Controls
- **Toggle** - Switch monitor on/off
- **Turn ON/OFF** - Direct control buttons

## 🔧 Advanced Setup

### Auto-Start Server on Mac Login

Create a LaunchAgent to start the server automatically:

```bash
# Create the plist file
cat > ~/Library/LaunchAgents/com.pdfmonitor.control.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.pdfmonitor.control</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app/ocr_control_server_enhanced.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app/logs/control_server.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app/logs/control_server.error.log</string>
</dict>
</plist>
EOF

# Load it
launchctl load ~/Library/LaunchAgents/com.pdfmonitor.control.plist
```

### Use Dynamic IP (Advanced)

If your Mac's IP changes frequently, you can:

1. **Set a static IP** in your router settings
2. **Use a service** like ngrok for external access
3. **Use mDNS** (Bonjour) - Access via `http://your-mac-name.local:5002`

## 🌐 API Endpoints

The server provides these endpoints:

### GET /api/status
Get current status:
```json
{
  "success": true,
  "status": "on",
  "running": true,
  "enabled": true,
  "stats": {
    "processed": 42,
    "errors": 0
  }
}
```

### POST /api/toggle
Toggle monitor on/off

### POST /api/on
Turn monitor on

### POST /api/off
Turn monitor off

### GET /api/stats
Get detailed statistics

### GET /api/folders
List monitored folders

## 🔒 Security Notes

- **Local Network Only** - Server only accessible on your local network
- **No Authentication** - Anyone on your network can control it
- **For Home Use** - Perfect for home/office networks

For production use, consider:
- Adding authentication
- Using HTTPS
- Restricting to specific IPs

## 🐛 Troubleshooting

### Widget Won't Load

1. **Check server is running**:
   ```bash
   ps aux | grep ocr_control_server_enhanced
   ```

2. **Check Mac firewall**:
   - System Settings → Network → Firewall
   - Allow incoming connections for Python

3. **Test in browser first**:
   - On Mac: `http://localhost:5002`
   - On iPhone: `http://YOUR_MAC_IP:5002`

### Can't Connect from iPhone

1. **Same network?** - Mac and iPhone must be on same Wi-Fi
2. **Check IP address** - IP might have changed
3. **Try Mac's hostname**: `http://your-mac-name.local:5002`

### Widget Shows Old Status

- Widget auto-refreshes every 10 seconds
- Pull down to refresh manually
- Check server is running

### Server Won't Start

1. **Check port 5002 is free**:
   ```bash
   lsof -i :5002
   ```

2. **Check Python dependencies**:
   ```bash
   pip3 install flask flask-cors
   ```

3. **Check logs**:
   ```bash
   tail -f logs/control_server.log
   ```

## 📊 Comparison: Widget vs Menu Bar

| Feature | iOS Widget | Menu Bar |
|---------|-----------|----------|
| Visibility | Always on home screen | May be hidden |
| Remote Control | Works from anywhere | Mac only |
| Status Display | Visual indicator | Text only |
| Statistics | Always visible | Click to see |
| Ease of Use | One tap | Multiple clicks |

## 🎨 Customization

The widget uses iOS-style design:
- **SF Pro Display** font (native iOS font)
- **iOS colors** - Green for ON, Red for OFF
- **Rounded corners** - iOS 14+ style
- **Touch-friendly** - Large buttons

## 💡 Tips

1. **Add to Dock** - Place widget in your iOS dock for quick access
2. **Use Siri Shortcuts** - Create Siri commands to control monitor
3. **Multiple Devices** - Add widget to iPad too
4. **Bookmark** - Bookmark the URL in Safari for quick access

## 🚀 Next Steps

1. ✅ Start the server
2. ✅ Add widget to home screen
3. ✅ Test toggle functionality
4. ✅ Set up auto-start (optional)
5. ✅ Enjoy remote control!

The widget is now ready to use! 🎉

