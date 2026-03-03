# PDF Monitor - Quick Start Guide

## Easy Desktop Access

### Start PDF Monitor
**Double-click:** `PDFMonitorLauncher.app` on your Desktop or in Applications

This will:
- Start the web control panel
- Open your browser automatically
- Show a notification when ready

### Stop PDF Monitor
**Double-click:** `PDFMonitorStop.app` on your Desktop or in Applications

This will:
- Stop all PDF Monitor processes
- Show a confirmation notification

## Add to Dock (Recommended)

1. **Find the apps:**
   - On Desktop: `PDFMonitorLauncher.app` and `PDFMonitorStop.app`
   - Or in Applications folder (Cmd+Shift+A)

2. **Drag to Dock:**
   - Drag `PDFMonitorLauncher.app` to your Dock
   - Drag `PDFMonitorStop.app` to your Dock

3. **Now you can:**
   - Click the launcher icon in Dock to start
   - Click the stop icon in Dock to stop

## Web Control Panel

Once started, access the control panel at:
**http://127.0.0.1:5000**

Features:
- Toggle monitoring ON/OFF
- View status and statistics
- See monitored folders
- Real-time updates

## Auto-Start on Login (Optional)

To automatically start PDF Monitor when you log in:

1. Open System Settings → Users & Groups → Login Items
2. Click the "+" button
3. Navigate to and select `PDFMonitorLauncher.app`
4. Check the box to enable it

## Manual Start (Terminal)

If you prefer command line:
```bash
cd /Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app
python3 pdf_monitor_web.py
```

## Troubleshooting

**App won't start?**
- Make sure Python 3 is installed
- Check that dependencies are installed: `pip3 install -r requirements.txt`

**Can't find the apps?**
- Run: `./create_desktop_launchers.sh` in the project folder
- Or manually copy the `.app` folders to Desktop

**Web interface not loading?**
- Make sure port 5000 isn't in use
- Try: `http://127.0.0.1:5000` instead of `localhost:5000`

