#!/bin/bash
# Start OCR Control Server for iOS Shortcuts

cd "$(dirname "$0")"

echo "🚀 Starting OCR Control Server..."
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask not found. Installing..."
    pip3 install flask flask-cors
fi

# Get Mac IP address
MAC_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

echo "📱 Server will be available at:"
echo "   Mac: http://localhost:5002"
echo "   iPhone: http://${MAC_IP}:5002"
echo ""
echo "📖 See IOS_WIDGET_SETUP.md for iOS Shortcuts setup"
echo ""
echo "Starting server..."
echo ""

python3 ocr_control_server.py


