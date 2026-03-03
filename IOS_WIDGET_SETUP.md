# iOS Widget/Shortcut Setup for OCR App

## Overview

iOS widgets can't directly control macOS apps, but we can use **iOS Shortcuts** with a simple web API to toggle the OCR monitor on/off.

## Solution: Web API + iOS Shortcuts

I've created a control server that provides a simple HTTP API. You can control it from:
- **iOS Shortcuts** (recommended - works like a widget)
- **Web browser** (on any device)
- **Siri** (via Shortcuts)

## Setup Steps

### 1. Start the Control Server

On your Mac, run:

```bash
cd /Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app
python3 ocr_control_server.py
```

Or add it to startup (see below).

The server runs on **port 5002**.

### 2. Find Your Mac's IP Address

```bash
# On your Mac, run:
ifconfig | grep "inet " | grep -v 127.0.0.1
```

You'll see something like: `192.168.1.100`

### 3. Create iOS Shortcut

1. **Open Shortcuts app** on your iPhone/iPad
2. **Tap "+"** to create new shortcut
3. **Add "Get Contents of URL"** action
4. **Set URL to**: `http://YOUR_MAC_IP:5002/api/toggle`
   - Replace `YOUR_MAC_IP` with your Mac's IP (e.g., `192.168.1.100`)
5. **Set Method to**: `POST`
6. **Add "Show Notification"** action
   - Set text to: "OCR Monitor toggled"
7. **Name the shortcut**: "Toggle OCR Monitor"
8. **Add to Home Screen** (optional - makes it widget-like)

### 4. Create ON/OFF Shortcuts (Optional)

Create separate shortcuts:
- **Turn ON**: `http://YOUR_MAC_IP:5002/api/on`
- **Turn OFF**: `http://YOUR_MAC_IP:5002/api/off`

## Using the Shortcut

### Method 1: Shortcuts App
1. Open Shortcuts app
2. Tap "Toggle OCR Monitor"
3. Done!

### Method 2: Home Screen Widget
1. Add shortcut to Home Screen
2. Tap the icon
3. Monitor toggles!

### Method 3: Siri
1. Say "Hey Siri, toggle OCR monitor"
2. (If you set up Siri shortcut)

## Web Interface

You can also use a web browser:

1. On your Mac: `http://localhost:5002`
2. On iPhone (same network): `http://YOUR_MAC_IP:5002`

The web interface has buttons to toggle the monitor.

## Auto-Start the Server

### Option 1: LaunchAgent (Recommended)

Create `~/Library/LaunchAgents/com.ocr.control.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ocr.control</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app/ocr_control_server.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Then load it:
```bash
launchctl load ~/Library/LaunchAgents/com.ocr.control.plist
```

### Option 2: Add to Login Items

1. System Settings → Users & Groups → Login Items
2. Add the script or create a simple app

## API Endpoints

### GET /api/status
Check current status:
```json
{
  "success": true,
  "status": "on",
  "running": true,
  "enabled": true
}
```

### POST /api/toggle
Toggle on/off:
```json
{
  "success": true,
  "status": "off",
  "message": "Monitor turned off"
}
```

### POST /api/on
Turn on:
```json
{
  "success": true,
  "status": "on",
  "message": "Monitor turned on"
}
```

### POST /api/off
Turn off:
```json
{
  "success": true,
  "status": "off",
  "message": "Monitor turned off"
}
```

## Troubleshooting

### Can't connect from iPhone

1. **Check firewall**: Allow port 5002 in System Settings → Firewall
2. **Check IP address**: Make sure Mac and iPhone are on same network
3. **Check server**: Make sure server is running on Mac

### Shortcut doesn't work

1. **Test in browser first**: `http://YOUR_MAC_IP:5002/api/status`
2. **Check URL**: Make sure it's `http://` not `https://`
3. **Check method**: Must be `POST` for toggle/on/off

### Server won't start

1. **Check port**: Make sure nothing else is using port 5002
2. **Check Python**: `python3 --version`
3. **Install Flask**: `pip install flask flask-cors`

## Advanced: Better Integration

For a more native iOS experience, you could:

1. **Use HomeKit** - Create a virtual switch that controls the monitor
2. **Use MQTT** - More robust for home automation
3. **Create native iOS app** - Full control, but more work

But the Shortcuts + Web API approach is the simplest and works great!

## Security Note

This server runs on your local network. For production use, consider:
- Adding authentication
- Using HTTPS
- Restricting to specific IPs

For home use, the current setup is fine.

## Quick Start Script

Save this as `start_ocr_control.sh`:

```bash
#!/bin/bash
cd /Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app
python3 ocr_control_server.py &
echo "OCR Control Server started on port 5002"
echo "Access at: http://localhost:5002"
echo "Or from iPhone: http://$(ifconfig | grep 'inet ' | grep -v 127.0.0.1 | awk '{print $2}' | head -1):5002"
```

Make it executable:
```bash
chmod +x start_ocr_control.sh
```

Then run: `./start_ocr_control.sh`


