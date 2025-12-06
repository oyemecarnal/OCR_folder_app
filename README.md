# PDF Folder Monitor

Automatically monitors folders for new PDF files and runs OCR on them, replacing the original files with OCR-enabled versions.

## Features

- **macOS Menu Bar App** - Beautiful menu bar interface with easy controls
- Monitor multiple folders for new PDF files
- Automatically run OCR on new PDFs when they appear
- Replace original files with OCR-enabled versions
- Track processed files to avoid reprocessing
- **On/Off Toggle** - Start and stop monitoring with one click
- **Pause/Resume** - Temporarily pause processing without stopping the monitor
- **Folder Management** - Quick access to up to 4 folders in the menu, with full management window
- **Statistics** - Track total processed files and errors
- Easy CLI tool to manage monitored folders (alternative to GUI)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Note: `ocrmypdf` requires Tesseract OCR to be installed on your system:
   - **macOS**: `brew install tesseract`
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
   - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Usage

### macOS Menu Bar App (Recommended)

The menu bar app provides a user-friendly interface to manage PDF monitoring:

1. **Start the app:**
   ```bash
   python pdf_monitor_app.py
   ```

2. **Access the menu bar:** Click the "PDF Monitor" icon in your macOS menu bar

3. **Menu options:**
   - **Monitor ON/OFF** - Toggle monitoring on or off
   - **Folders** - Quick access to your monitored folders (shows up to 4, click to open in Finder)
     - If you have 4 or more folders, the 5th option "Manage All Folders..." opens the full preferences window
   - **Pause/Resume** - Temporarily pause processing (monitor stays running)
   - **Statistics** - View total processed files and errors
   - **Preferences...** - Full folder management window where you can:
     - Add new folders to monitor
     - Remove folders from monitoring
     - See all monitored folders in a list

4. **Features:**
   - The app runs in the background and stays in the menu bar
   - Notifications inform you when monitoring starts/stops/pauses
   - Quick access to folders directly from the menu
   - Statistics tracking for processed files

### Command Line Interface (Alternative)

You can also use the command-line version:

**Starting the Monitor:**

Run the monitoring service:
```bash
python pdf_monitor.py
```

The monitor will:
- Load the default folder (`/Users/kevinreed/Downloads`) if no folders are configured
- Watch for new PDF files in all configured folders
- Automatically process PDFs when they appear
- Log activity to `pdf_monitor.log` and the console

**Managing Monitored Folders:**

Use the `manage_folders.py` script to add or remove folders:

**Add a folder:**
```bash
python manage_folders.py add /path/to/folder
python manage_folders.py add ~/Documents/Inbox
```

**Remove a folder:**
```bash
python manage_folders.py remove /path/to/folder
```

**List monitored folders:**
```bash
python manage_folders.py list
```

### Example Workflow

1. Start the monitor:
   ```bash
   python pdf_monitor.py
   ```

2. Add additional folders (in another terminal):
   ```bash
   python manage_folders.py add ~/Desktop/Scans
   python manage_folders.py add ~/Documents/PDFs
   ```

3. Drop PDF files into any monitored folder - they will be automatically processed!

## How It Works

- The monitor uses file system events to detect when new PDFs are added
- Files are checked to ensure they're completely written before processing
- OCR is performed using `ocrmypdf`, which embeds searchable text into PDFs
- Original files are replaced with the OCR-enabled version
- Processed files are tracked to avoid reprocessing
- If a PDF already has an OCR text layer, it's skipped

## Files

- `pdf_monitor_app.py` - **macOS menu bar application** (recommended)
- `pdf_monitor.py` - Main monitoring service (core functionality)
- `manage_folders.py` - CLI tool for managing folders
- `monitored_folders.json` - Configuration file (auto-generated)
- `processed_pdfs.txt` - Log of processed files (auto-generated)
- `monitor_stats.json` - Statistics file (auto-generated)
- `pdf_monitor.log` - Application log file (auto-generated)

## Notes

- The monitor processes PDFs in the order they appear
- Large PDFs may take some time to process
- The original file is replaced, so ensure you have backups if needed
- The monitor runs continuously until stopped (Ctrl+C)

