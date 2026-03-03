#!/usr/bin/env python3
"""
Enhanced OCR Control Server with Direct Monitor Control

This server provides a REST API to control the PDF Monitor app directly,
without needing the menu bar. Perfect for iOS widgets and remote control.
"""

import os
import json
import subprocess
import sys
import signal
import time
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow iOS Shortcuts/widgets to call this

CONFIG_FILE = Path(__file__).parent / 'monitored_folders.json'
CONTROL_FILE = Path(__file__).parent / '.ocr_control.json'
MONITOR_PID_FILE = Path(__file__).parent / '.pdf_monitor.pid'
STATS_FILE = Path(__file__).parent / 'monitor_stats.json'

# Global reference to monitor process
monitor_process = None
monitor_script_path = Path(__file__).parent / 'pdf_monitor_app.py'


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
    
    # Get statistics
    stats = {'processed': 0, 'errors': 0, 'last_processed': None}
    if STATS_FILE.exists():
        try:
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
        except:
            pass
    
    return {
        'running': process_running,
        'enabled': enabled,
        'status': 'on' if (process_running and enabled) else 'off',
        'stats': stats
    }


def start_monitor():
    """Start the PDF monitor app or enable monitoring if already running."""
    global monitor_process
    
    status = get_monitor_status()
    
    # If app is running, just enable monitoring via config
    if status['running']:
        try:
            # Enable monitoring in config (app will pick this up)
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                config['monitor_enabled'] = True
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(config, f, indent=2)
            
            # Write control file to trigger start
            control_data = {'action': 'start', 'timestamp': time.time()}
            with open(CONTROL_FILE, 'w') as f:
                json.dump(control_data, f)
            
            return {'success': True, 'message': 'Monitoring enabled'}
        except Exception as e:
            return {'success': False, 'message': f'Error enabling monitor: {str(e)}'}
    
    # App not running, start it
    try:
        # Start the monitor app
        monitor_process = subprocess.Popen(
            [sys.executable, str(monitor_script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(monitor_script_path.parent)
        )
        
        # Save PID
        with open(MONITOR_PID_FILE, 'w') as f:
            f.write(str(monitor_process.pid))
        
        # Wait a moment for it to start
        time.sleep(2)
        
        # Enable monitoring in config
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            config['monitor_enabled'] = True
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
        
        return {'success': True, 'message': 'Monitor started'}
    except Exception as e:
        return {'success': False, 'message': f'Error starting monitor: {str(e)}'}


def stop_monitor():
    """Stop monitoring (but keep app running) or stop app if needed."""
    global monitor_process
    
    status = get_monitor_status()
    
    try:
        # Disable monitoring in config
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            config['monitor_enabled'] = False
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
        
        # Write control file to trigger stop
        control_data = {'action': 'stop', 'timestamp': time.time()}
        with open(CONTROL_FILE, 'w') as f:
            json.dump(control_data, f)
        
        # If user wants to completely stop the app, uncomment below:
        # result = subprocess.run(
        #     ['pkill', '-f', 'pdf_monitor_app.py'],
        #     capture_output=True,
        #     text=True
        # )
        # if MONITOR_PID_FILE.exists():
        #     MONITOR_PID_FILE.unlink()
        # monitor_process = None
        
        return {'success': True, 'message': 'Monitoring disabled'}
    except Exception as e:
        return {'success': False, 'message': f'Error stopping monitor: {str(e)}'}


def toggle_monitor():
    """Toggle monitor on/off."""
    status = get_monitor_status()
    if status['status'] == 'on':
        return stop_monitor()
    else:
        return start_monitor()


@app.route('/api/status', methods=['GET'])
def api_status():
    """Get current monitor status with detailed info."""
    status = get_monitor_status()
    return jsonify({
        'success': True,
        'status': status['status'],
        'running': status['running'],
        'enabled': status['enabled'],
        'stats': status['stats']
    })


@app.route('/api/toggle', methods=['POST'])
def api_toggle():
    """Toggle monitor on/off."""
    result = toggle_monitor()
    status = get_monitor_status()
    return jsonify({
        'success': result['success'],
        'status': status['status'],
        'message': result['message']
    })


@app.route('/api/on', methods=['POST'])
def api_on():
    """Turn monitor on."""
    result = start_monitor()
    status = get_monitor_status()
    return jsonify({
        'success': result['success'],
        'status': status['status'],
        'message': result['message']
    })


@app.route('/api/off', methods=['POST'])
def api_off():
    """Turn monitor off."""
    result = stop_monitor()
    status = get_monitor_status()
    return jsonify({
        'success': result['success'],
        'status': status['status'],
        'message': result['message']
    })


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get detailed statistics."""
    status = get_monitor_status()
    return jsonify({
        'success': True,
        'stats': status['stats'],
        'status': status['status']
    })


@app.route('/api/folders', methods=['GET'])
def api_folders():
    """Get list of monitored folders."""
    folders = []
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                folders = config.get('folders', [])
        except:
            pass
    return jsonify({
        'success': True,
        'folders': folders,
        'count': len(folders)
    })


@app.route('/api/health', methods=['GET'])
def api_health():
    """Health check."""
    return jsonify({
        'status': 'healthy',
        'service': 'OCR Control Server Enhanced',
        'version': '2.0'
    })


@app.route('/', methods=['GET'])
def index():
    """iOS-optimized web widget interface."""
    status = get_monitor_status()
    status_text = 'ON' if status['status'] == 'on' else 'OFF'
    status_color = '#34C759' if status['status'] == 'on' else '#FF3B30'
    bg_color = '#F2F2F7' if status['status'] == 'on' else '#1C1C1E'
    text_color = '#000000' if status['status'] == 'on' else '#FFFFFF'
    
    stats = status['stats']
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <title>PDF Monitor</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
                background: {bg_color};
                color: {text_color};
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .widget {{
                background: {'#FFFFFF' if status['status'] == 'on' else '#2C2C2E'};
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                max-width: 400px;
                width: 100%;
                text-align: center;
            }}
            .status-indicator {{
                width: 80px;
                height: 80px;
                border-radius: 50%;
                background: {status_color};
                margin: 0 auto 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 40px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            }}
            .status-text {{
                font-size: 32px;
                font-weight: 700;
                margin-bottom: 10px;
                color: {status_color};
            }}
            .stats {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin: 25px 0;
            }}
            .stat-item {{
                background: {'#F2F2F7' if status['status'] == 'on' else '#1C1C1E'};
                padding: 15px;
                border-radius: 12px;
            }}
            .stat-value {{
                font-size: 24px;
                font-weight: 700;
                color: {status_color};
            }}
            .stat-label {{
                font-size: 12px;
                color: {'#666' if status['status'] == 'on' else '#999'};
                margin-top: 5px;
            }}
            .buttons {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-top: 20px;
            }}
            button {{
                background: {status_color};
                color: white;
                border: none;
                padding: 15px;
                font-size: 16px;
                font-weight: 600;
                border-radius: 12px;
                cursor: pointer;
                transition: transform 0.2s, opacity 0.2s;
            }}
            button:active {{
                transform: scale(0.95);
                opacity: 0.8;
            }}
            .btn-secondary {{
                background: {'#E5E5EA' if status['status'] == 'on' else '#3A3A3C'};
                color: {text_color};
            }}
            .info {{
                margin-top: 20px;
                font-size: 12px;
                color: {'#666' if status['status'] == 'on' else '#999'};
            }}
        </style>
    </head>
    <body>
        <div class="widget">
            <div class="status-indicator">
                {'✓' if status['status'] == 'on' else '○'}
            </div>
            <div class="status-text">{status_text}</div>
            <div class="info">PDF Monitor</div>
            
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value">{stats.get('processed', 0)}</div>
                    <div class="stat-label">Processed</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{stats.get('errors', 0)}</div>
                    <div class="stat-label">Errors</div>
                </div>
            </div>
            
            <div class="buttons">
                <button onclick="toggle()" class="btn-primary">Toggle</button>
                <button onclick="{'turnOff()' if status['status'] == 'on' else 'turnOn()'}" class="btn-secondary">
                    {'Turn OFF' if status['status'] == 'on' else 'Turn ON'}
                </button>
            </div>
            
            <div class="info">
                Tap "Add to Home Screen" to use as widget
            </div>
        </div>
        
        <script>
            function toggle() {{
                fetch('/api/toggle', {{method: 'POST'}})
                    .then(r => r.json())
                    .then(data => {{
                        if (data.success) {{
                            setTimeout(() => location.reload(), 500);
                        }} else {{
                            alert('Error: ' + data.message);
                        }}
                    }})
                    .catch(err => alert('Error: ' + err));
            }}
            function turnOn() {{
                fetch('/api/on', {{method: 'POST'}})
                    .then(r => r.json())
                    .then(data => {{
                        if (data.success) {{
                            setTimeout(() => location.reload(), 500);
                        }} else {{
                            alert('Error: ' + data.message);
                        }}
                    }})
                    .catch(err => alert('Error: ' + err));
            }}
            function turnOff() {{
                fetch('/api/off', {{method: 'POST'}})
                    .then(r => r.json())
                    .then(data => {{
                        if (data.success) {{
                            setTimeout(() => location.reload(), 500);
                        }} else {{
                            alert('Error: ' + data.message);
                        }}
                    }})
                    .catch(err => alert('Error: ' + err));
            }}
            
            // Auto-refresh every 10 seconds
            setInterval(() => {{
                fetch('/api/status')
                    .then(r => r.json())
                    .then(data => {{
                        if (data.status !== '{status['status']}') {{
                            location.reload();
                        }}
                    }});
            }}, 10000);
        </script>
    </body>
    </html>
    '''
    return html


if __name__ == '__main__':
    print("=" * 60)
    print("Enhanced OCR Control Server")
    print("=" * 60)
    print()
    print("🌐 Web Widget: http://localhost:5002")
    print("📱 iOS Widget: Add to Home Screen from Safari")
    print()
    print("API Endpoints:")
    print("  GET  /api/status  - Check status")
    print("  GET  /api/stats    - Get statistics")
    print("  GET  /api/folders - List folders")
    print("  POST /api/toggle  - Toggle on/off")
    print("  POST /api/on      - Turn on")
    print("  POST /api/off     - Turn off")
    print()
    print("Starting server on port 5002...")
    print()
    
    app.run(host='0.0.0.0', port=5002, debug=False)

