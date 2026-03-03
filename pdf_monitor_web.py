#!/usr/bin/env python3
"""
Web-based control panel for PDF Monitor
Provides a browser-accessible interface when menu bar doesn't show
"""
from flask import Flask, render_template_string, jsonify, request
import threading
import webbrowser
import time
from pdf_monitor import PDFMonitor, ConfigManager, logger

app = Flask(__name__)
monitor = None
stats = {'processed': 0, 'errors': 0}

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PDF Monitor Control Panel</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .content { padding: 30px; }
        .status {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        .status-on { background: #4CAF50; }
        .status-off { background: #f44336; }
        .status-paused { background: #ff9800; }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
            transition: transform 0.2s;
        }
        .btn:hover { transform: scale(1.05); }
        .btn-danger { background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%); }
        .btn-success { background: linear-gradient(135deg, #4CAF50 0%, #2e7d32 100%); }
        .folders {
            margin: 20px 0;
        }
        .folder-item {
            background: #f9f9f9;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-value {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }
        .log {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Monaco', monospace;
            font-size: 12px;
            max-height: 200px;
            overflow-y: auto;
            margin-top: 20px;
        }
    </style>
    <script>
        function updateStatus() {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('status-text').innerHTML = 
                        '<span class="status-indicator status-' + data.status + '"></span>' + data.statusText;
                    document.getElementById('folders-count').textContent = data.folders_count;
                    document.getElementById('processed-count').textContent = data.stats.processed;
                    document.getElementById('errors-count').textContent = data.stats.errors;
                });
            setTimeout(updateStatus, 2000);
        }
        function toggleMonitor() {
            fetch('/api/toggle', {method: 'POST'})
                .then(r => r.json())
                .then(data => {
                    alert(data.message);
                    updateStatus();
                });
        }
        function togglePause() {
            fetch('/api/pause', {method: 'POST'})
                .then(r => r.json())
                .then(data => {
                    alert(data.message);
                    updateStatus();
                });
        }
        window.onload = function() {
            updateStatus();
            fetch('/api/folders')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('folders-list');
                    container.innerHTML = data.folders.map(f => 
                        '<div class="folder-item"><span>' + f + '</span></div>'
                    ).join('');
                });
        };
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📄 PDF Monitor</h1>
            <p>Control Panel</p>
        </div>
        <div class="content">
            <div class="status">
                <div>
                    <strong>Status:</strong> <span id="status-text">Loading...</span>
                </div>
                <div>
                    <button class="btn btn-success" onclick="toggleMonitor()">Toggle Monitor</button>
                    <button class="btn" onclick="togglePause()">Pause/Resume</button>
                </div>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value" id="folders-count">0</div>
                    <div>Folders Monitored</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="processed-count">0</div>
                    <div>Files Processed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="errors-count">0</div>
                    <div>Errors</div>
                </div>
            </div>
            
            <div class="folders">
                <h3>Monitored Folders</h3>
                <div id="folders-list"></div>
            </div>
            
            <div>
                <p><strong>Note:</strong> This web interface is running because the menu bar item isn't visible. 
                The monitor is working in the background. You can manage folders using the CLI tool:</p>
                <code>python3 manage_folders.py list</code>
            </div>
        </div>
    </div>
</body>
</html>
"""

def init_monitor():
    global monitor
    if monitor is None:
        try:
            monitor = PDFMonitor()
        except Exception as e:
            logger.error(f"Error initializing monitor: {e}")
            monitor = None

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def api_status():
    if monitor is None:
        init_monitor()
    
    status = 'off'
    status_text = 'Monitor OFF'
    if monitor and monitor.running:
        status = 'on'
        status_text = 'Monitor ON'
    
    return jsonify({
        'status': status,
        'statusText': status_text,
        'folders_count': len(monitor.config_manager.list_folders()) if monitor else 0,
        'stats': stats
    })

@app.route('/api/toggle', methods=['POST'])
def api_toggle():
    if monitor is None:
        init_monitor()
    
    if not monitor:
        return jsonify({'message': 'Error: Monitor not initialized'}), 500
    
    if monitor.running:
        monitor.stop()
        return jsonify({'message': 'Monitor stopped'})
    else:
        monitor.start()
        return jsonify({'message': 'Monitor started'})

@app.route('/api/pause', methods=['POST'])
def api_pause():
    return jsonify({'message': 'Pause/resume not yet implemented in web interface'})

@app.route('/api/folders')
def api_folders():
    if monitor is None:
        init_monitor()
    folders = monitor.config_manager.list_folders() if monitor else []
    return jsonify({'folders': folders})

def start_server(port=5000):
    time.sleep(2)  # Wait a moment for server to start
    try:
        webbrowser.open(f'http://127.0.0.1:{port}')
    except:
        print(f"Please open http://127.0.0.1:{port} in your browser")

if __name__ == '__main__':
    print("Starting PDF Monitor Web Control Panel...")
    init_monitor()
    print("Server starting at http://127.0.0.1:5000")
    print("Opening browser...")
    threading.Thread(target=start_server, daemon=True).start()
    try:
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port 5000 is already in use. Trying port 5001...")
            threading.Thread(target=lambda: time.sleep(2) or webbrowser.open('http://127.0.0.1:5001'), daemon=True).start()
            app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)
        else:
            raise

