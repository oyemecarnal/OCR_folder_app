#!/bin/bash
# Start the iOS Widget Control Server

cd "$(dirname "$0")"

echo "🚀 Starting PDF Monitor iOS Widget Server..."
echo ""

# Check if already running
if ps aux | grep -i "ocr_control_server_enhanced" | grep -v grep > /dev/null; then
    echo "⚠️  Server is already running!"
    echo "   Stop it first with: pkill -f ocr_control_server_enhanced"
    exit 1
fi

# Get Mac IP address
MAC_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

echo "📱 Server will be available at:"
echo "   Mac: http://localhost:5002"
echo "   iOS: http://${MAC_IP}:5002"
echo ""
echo "📋 To add widget to iOS:"
echo "   1. Open Safari on iPhone/iPad"
echo "   2. Go to: http://${MAC_IP}:5002"
echo "   3. Tap Share → Add to Home Screen"
echo ""
echo "Starting server..."
echo ""

# Start the server
python3 ocr_control_server_enhanced.py

