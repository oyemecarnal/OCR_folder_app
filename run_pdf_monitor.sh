#!/bin/bash
cd "/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app"
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"

echo "🚀 Starting PDF Monitor..."
echo "📋 Look for 'PDF Monitor' in your menu bar (top right)"
echo "   If you don't see it, check the overflow menu (>> arrow)"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 pdf_monitor_app.py
