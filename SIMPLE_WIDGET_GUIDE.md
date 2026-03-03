# Simple PDF Monitor Widget - User Guide

## 🎯 What It Does

A simple macOS widget that:
- ✅ Toggles monitoring ON/OFF
- ✅ Lets you select a folder to monitor
- ✅ Processes PDFs placed in folder within X hours (default: 1 hour)
- ✅ Has a "Process Now" button for immediate processing

## 🚀 Quick Start

### Step 1: Launch the Widget

```bash
open PDFMonitorWidget.app
```

Or double-click `PDFMonitorWidget.app` in Finder.

### Step 2: Select Folder

1. Click **"Select Folder"** button
2. Choose the folder you want to monitor
3. Folder path will be displayed

### Step 3: Set Time (Optional)

- Default is **1 hour**
- Adjust the spinner to change (0.1 to 24 hours)
- Files newer than this time will be processed

### Step 4: Start Monitoring

1. Click **"Start Monitoring"** button
2. Status changes to **"ON"** (green)
3. Widget will automatically process PDFs placed in the folder

## 📋 Features

### Toggle ON/OFF
- Click "Start Monitoring" to begin
- Click "Stop Monitoring" to pause
- Status shows ON (green) or OFF (red)

### Select Folder
- Click "Select Folder" button
- Choose any folder on your Mac
- Widget remembers your selection

### Time Setting
- Default: 1 hour
- Range: 0.1 to 24 hours
- Only files newer than this will be processed
- Example: Set to 0.5 hours = process files < 30 minutes old

### Process Now
- Click "Process Now" to immediately process all matching files
- Useful for testing or one-time processing
- Processes files that match your time criteria

## 🔧 How It Works

1. **Monitoring**: Checks folder every 30 seconds
2. **File Detection**: Finds PDF files
3. **Age Check**: Only processes files newer than your setting
4. **OCR Processing**: Runs OCR on matching files
5. **Replacement**: Replaces original with OCR-enabled version

## 💾 Configuration

Settings are saved in `widget_config.json`:
- `folder`: Selected folder path
- `max_age_hours`: Time threshold (default: 1)
- `monitoring`: Current monitoring state

## 🐛 Troubleshooting

### Widget Won't Open
- Check Python 3 is installed: `python3 --version`
- Check dependencies: `pip3 install ocrmypdf`

### OCR Not Working
- Make sure Tesseract is installed: `brew install tesseract`
- Check file permissions on selected folder

### Files Not Processing
- Make sure monitoring is ON (green status)
- Check files are PDFs (.pdf extension)
- Verify files are newer than your time setting
- Check folder path is correct

### Widget Closes Unexpectedly
- Check console for error messages
- Make sure folder still exists
- Verify Python dependencies are installed

## 📝 Example Workflow

1. **Launch widget**: Double-click PDFMonitorWidget.app
2. **Select folder**: Click "Select Folder" → Choose "~/Downloads"
3. **Set time**: Keep default 1 hour (or change to 0.5 for 30 minutes)
4. **Start monitoring**: Click "Start Monitoring"
5. **Drop PDFs**: Place PDF files in ~/Downloads
6. **Auto-processing**: Files < 1 hour old are automatically processed
7. **Check results**: Original PDFs are replaced with OCR-enabled versions

## 🎨 Customization

### Change Default Time
Edit `pdf_monitor_widget.py`:
```python
self.config = {
    'folder': '',
    'max_age_hours': 1,  # Change this
    'monitoring': False
}
```

### Change Check Interval
Edit the `monitor_loop` function:
```python
time.sleep(30)  # Change 30 to desired seconds
```

## ✅ That's It!

This is a simple, focused widget that does exactly what you need:
- Toggle on/off ✓
- Select folder ✓
- Process files < 1 hour old ✓
- Customizable time setting ✓

No complex setup, no dependencies on other servers - just a simple, working widget!

