# Menu Bar Visibility Troubleshooting Guide

## Quick Checks

### 1. Is the app running?
```bash
ps aux | grep pdf_monitor_app | grep -v grep
```
If you see a process, the app IS running.

### 2. Check menu bar overflow area
- Look at the **far right** of your menu bar
- Click the **>> (double chevron)** icon
- This is where hidden menu bar items go when space is limited

### 3. Restart SystemUIServer
```bash
killall SystemUIServer
```
This refreshes the menu bar without restarting your Mac.

### 4. Check menu bar space
- macOS hides menu bar items when space is limited
- Especially on MacBooks with camera notch
- Try removing other menu bar items temporarily

## Deep Dive Solutions

### Solution 1: Force Menu Bar Refresh
```bash
# Stop the app
pkill -f pdf_monitor_app

# Restart menu bar
killall SystemUIServer

# Wait 2 seconds, then restart app
sleep 2
python3 pdf_monitor_app.py
```

### Solution 2: Run as App Bundle
Instead of running the Python script directly, use the app bundle:
```bash
open PDFMonitor.app
```
Or double-click `PDFMonitor.app` in Finder.

### Solution 3: Check macOS Permissions
1. Open **System Settings** → **Privacy & Security**
2. Check **Accessibility** - Python might need permission
3. Check **Automation** - App might need permission to control system

### Solution 4: Reduce Menu Bar Clutter
1. Go to **System Settings** → **Control Center**
2. Hide unnecessary icons to free up space
3. Menu bar items are hidden when space runs out

### Solution 5: Use Test Script
Run the test script to verify rumps is working:
```bash
python3 test_menu_visibility.py
```
If you see "🧪 TEST" in menu bar, rumps works. If not, it's a macOS/system issue.

### Solution 6: Check Console Logs
```bash
# View recent app logs
tail -50 logs/pdf_monitor_app.log

# Check for errors
grep -i error logs/pdf_monitor_app.log
```

### Solution 7: Alternative - Use Web Interface
If menu bar doesn't work, use the web interface:
```bash
python3 pdf_monitor_web.py
```
Then open: http://127.0.0.1:5000

## Why Menu Bar Items Hide

1. **Space Constraints**: macOS automatically hides items when menu bar is full
2. **Camera Notch**: MacBooks with notch have less menu bar space
3. **System Preferences**: Some items are hidden by default
4. **Priority**: System items take priority over third-party apps

## Verification Steps

1. ✅ App is running (check with `ps aux`)
2. ✅ No errors in logs
3. ✅ Checked overflow area (>> icon)
4. ✅ Restarted SystemUIServer
5. ✅ Freed up menu bar space
6. ✅ Checked macOS permissions

## Still Not Working?

If the app is running but menu bar item isn't visible:

1. **The app still works** - It processes PDFs in the background
2. **Use CLI tools** - `python3 manage_folders.py list`
3. **Use web interface** - `python3 pdf_monitor_web.py`
4. **Check notifications** - App sends notifications when processing

The menu bar item is a convenience feature - the core functionality works without it!

