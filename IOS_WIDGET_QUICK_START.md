# iOS Widget - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Start the Server (Mac)

```bash
cd /Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app
./start_ios_widget_server.sh
```

The server will show your Mac's IP address.

### Step 2: Add Widget (iPhone/iPad)

1. Open **Safari** on your iPhone/iPad
2. Go to: `http://YOUR_MAC_IP:5002` (use the IP shown in Step 1)
3. Tap **Share** button (square with arrow)
4. Tap **"Add to Home Screen"**
5. Tap **"Add"**

### Step 3: Use It!

Tap the widget on your home screen to control the PDF Monitor!

## ✨ What You Get

- **Visual Status** - Green = ON, Red = OFF
- **Statistics** - See processed files and errors
- **One-Tap Control** - Toggle monitor on/off
- **Auto-Updates** - Refreshes every 10 seconds

## 📱 Features

- Native iOS design
- Works from anywhere on your network
- No app installation needed
- Free and open source

## 🆘 Troubleshooting

**Can't connect?**
- Make sure Mac and iPhone are on same Wi-Fi
- Check Mac firewall allows Python
- Verify server is running: `ps aux | grep ocr_control_server_enhanced`

**Widget not updating?**
- Pull down to refresh
- Check server is still running
- Restart server if needed

## 📖 Full Guide

See `IOS_WIDGET_SETUP_V2.md` for complete documentation.

