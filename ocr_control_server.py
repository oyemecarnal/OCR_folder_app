#!/usr/bin/env python3
"""
OCR App Control Server

Simple HTTP API to control the OCR monitor from iOS Shortcuts or web.
Run this server, then use iOS Shortcuts to toggle the monitor on/off.
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow iOS Shortcuts to call this

CONFIG_FILE = Path(__file__).parent / 'monitored_folders.json'
CONTROL_FILE = Path(__file__).parent / '.ocr_control.json'


def get_monitor_status():
    """Check if monitor is running and enabled."""
    # Check if process is running
    result = subprocess.run(
        ['pgrep', '-f', 'pdf_monitor_app.py'],
        capture_output=True,
        text=True
    )
    process_running = result.returncode == 0
    
    # Check config file for enabled state
    enabled = False
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                enabled = config.get('monitor_enabled', False)
        except:
            pass
    
    return {
        'running': process_running,
        'enabled': enabled,
        'status': 'on' if (process_running and enabled) else 'off'
    }


def toggle_monitor():
    """Toggle monitor on/off by sending command to running app."""
    # Read current control state
    control_state = {'action': 'toggle'}
    
    # Write control file that the app can check
    with open(CONTROL_FILE, 'w') as f:
        json.dump(control_state, f)
    
    # Try to send AppleScript command to the app
    # This works if the app is running
    applescript = '''
    tell application "System Events"
        tell process "Python"
            try
                click menu item "Monitor ON" of menu 1 of menu bar item "PDF Monitor" of menu bar 1
            on error
                try
                    click menu item "Monitor OFF" of menu 1 of menu bar item "PDF Monitor" of menu bar 1
                end try
            end try
        end tell
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', applescript], 
                      capture_output=True, timeout=2)
    except:
        pass  # If app not running, that's okay
    
    return get_monitor_status()


@app.route('/api/status', methods=['GET'])
def status():
    """Get current monitor status."""
    status = get_monitor_status()
    return jsonify({
        'success': True,
        'status': status['status'],
        'running': status['running'],
        'enabled': status['enabled']
    })


@app.route('/api/toggle', methods=['POST'])
def toggle():
    """Toggle monitor on/off."""
    result = toggle_monitor()
    return jsonify({
        'success': True,
        'status': result['status'],
        'message': f"Monitor turned {result['status']}"
    })


@app.route('/api/on', methods=['POST'])
def turn_on():
    """Turn monitor on."""
    current = get_monitor_status()
    if current['status'] == 'off':
        toggle_monitor()
    return jsonify({
        'success': True,
        'status': 'on',
        'message': 'Monitor turned on'
    })


@app.route('/api/off', methods=['POST'])
def turn_off():
    """Turn monitor off."""
    current = get_monitor_status()
    if current['status'] == 'on':
        toggle_monitor()
    return jsonify({
        'success': True,
        'status': 'off',
        'message': 'Monitor turned off'
    })


@app.route('/api/health', methods=['GET'])
def health():
    """Health check."""
    return jsonify({
        'status': 'healthy',
        'service': 'OCR Control Server'
    })


@app.route('/', methods=['GET'])
def index():
    """Simple web interface for control."""
    status = get_monitor_status()
    status_text = 'ON' if status['status'] == 'on' else 'OFF'
    status_color = '#4CAF50' if status['status'] == 'on' else '#f44336'
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OCR Monitor Control</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                max-width: 400px;
                margin: 50px auto;
                padding: 20px;
                text-align: center;
            }}
            .status {{
                font-size: 48px;
                font-weight: bold;
                color: {status_color};
                margin: 20px 0;
            }}
            button {{
                background: #007AFF;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 18px;
                border-radius: 10px;
                cursor: pointer;
                margin: 10px;
                width: 200px;
            }}
            button:hover {{
                background: #0056CC;
            }}
            .info {{
                margin-top: 30px;
                color: #666;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <h1>OCR Monitor Control</h1>
        <div class="status">{status_text}</div>
        <button onclick="toggle()">Toggle</button>
        <button onclick="turnOn()">Turn ON</button>
        <button onclick="turnOff()">Turn OFF</button>
        <div class="info">
            <p>Status: {status['status']}</p>
            <p>Process: {'Running' if status['running'] else 'Not Running'}</p>
        </div>
        <script>
            function toggle() {{
                fetch('/api/toggle', {{method: 'POST'}})
                    .then(r => r.json())
                    .then(data => {{
                        alert(data.message);
                        location.reload();
                    }});
            }}
            function turnOn() {{
                fetch('/api/on', {{method: 'POST'}})
                    .then(r => r.json())
                    .then(data => {{
                        alert(data.message);
                        location.reload();
                    }});
            }}
            function turnOff() {{
                fetch('/api/off', {{method: 'POST'}})
                    .then(r => r.json())
                    .then(data => {{
                        alert(data.message);
                        location.reload();
                    }});
            }}
        </script>
    </body>
    </html>
    '''
    return html


if __name__ == '__main__':
    print("=" * 60)
    print("OCR Control Server")
    print("=" * 60)
    print()
    print("🌐 Web Interface: http://localhost:5002")
    print("📱 iOS Shortcuts: Use URLs below")
    print()
    print("Endpoints:")
    print("  GET  /api/status  - Check status")
    print("  POST /api/toggle  - Toggle on/off")
    print("  POST /api/on      - Turn on")
    print("  POST /api/off     - Turn off")
    print()
    print("For iOS Shortcuts:")
    print("  URL: http://YOUR_MAC_IP:5002/api/toggle")
    print("  Method: POST")
    print()
    print("Starting server on port 5002...")
    print()
    
    app.run(host='0.0.0.0', port=5002, debug=False)


