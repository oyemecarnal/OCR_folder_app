# Run PDF Monitor on This Machine

## One-time setup

```bash
cd /Users/kevinreed/dev/OCR_folder_app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install Tesseract if needed: `brew install tesseract`

## Run the menu bar app (interactive)

```bash
cd /Users/kevinreed/dev/OCR_folder_app
source .venv/bin/activate   # if using venv
python3 pdf_monitor_app.py
```

Look for **📄 PDF Monitor** in the menu bar (top right; check overflow >> if needed).

## Run at login (launchd)

```bash
# Copy plist to LaunchAgents (path in plist is already set for this repo)
cp /Users/kevinreed/dev/OCR_folder_app/com.kevinreed.pdfmonitor.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.kevinreed.pdfmonitor.plist
```

To stop: `launchctl unload ~/Library/LaunchAgents/com.kevinreed.pdfmonitor.plist`

## CLI (no menu bar)

```bash
python3 manage_folders.py list
python3 manage_folders.py add ~/Downloads
python3 pdf_monitor.py
```
