#!/usr/bin/env python3
"""
Enhanced PDF Monitor Dashboard with Live Data Feeds and Widgets
Supports API integrations and real-time updates
"""
from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import threading
import webbrowser
import time
import json
import os
import psutil
from datetime import datetime
from pdf_monitor import PDFMonitor, ConfigManager, logger

app = Flask(__name__)
CORS(app)  # Enable CORS for API access
monitor = None
stats = {'processed': 0, 'errors': 0, 'last_processed': None}

# Enhanced HTML template with widget support
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PDF Monitor Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f0f0f0;
            padding: 20px;
            min-height: 100vh;
        }
        .dashboard {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .widget-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .widget {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .widget:hover { transform: translateY(-2px); }
        .widget-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }
        .widget-title {
            font-size: 18px;
            font-weight: 600;
            color: #333;
        }
        .widget-icon { font-size: 24px; }
        .status-widget {
            border-left: 4px solid #4CAF50;
        }
        .status-widget.off { border-left-color: #f44336; }
        .status-widget.paused { border-left-color: #ff9800; }
        .stat-value {
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }
        .stat-label {
            color: #666;
            font-size: 14px;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            margin: 5px;
            transition: all 0.2s;
        }
        .btn:hover { transform: scale(1.05); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        .btn-danger { background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%); }
        .btn-success { background: linear-gradient(135deg, #4CAF50 0%, #2e7d32 100%); }
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .status-on { background: #4CAF50; }
        .status-off { background: #f44336; }
        .status-paused { background: #ff9800; }
        .log-widget {
            max-height: 200px;
            overflow-y: auto;
            font-family: 'Monaco', monospace;
            font-size: 12px;
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 8px;
        }
        .log-entry {
            margin: 5px 0;
            padding: 5px;
            border-left: 2px solid #667eea;
            padding-left: 10px;
        }
        .api-widget {
            min-height: 150px;
        }
        .api-status {
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            background: #f5f5f5;
        }
        .api-status.success { background: #e8f5e9; }
        .api-status.error { background: #ffebee; }
        .folder-list {
            max-height: 200px;
            overflow-y: auto;
        }
        .folder-item {
            padding: 10px;
            margin: 5px 0;
            background: #f5f5f5;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
        }
        .system-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 10px;
        }
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s;
        }
    </style>
    <script>
        let updateInterval;
        
        function updateDashboard() {
            // Update all widgets
            updateStatus();
            updateStats();
            updateSystemStats();
            updateActivityLog();
            updateAPIs();
        }
        
        function updateStatus() {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {
                    const widget = document.getElementById('status-widget');
                    widget.className = 'widget status-widget ' + data.status;
                    document.getElementById('status-text').innerHTML = 
                        '<span class="status-indicator status-' + data.status + '"></span>' + data.statusText;
                    document.getElementById('folders-count').textContent = data.folders_count;
                });
        }
        
        function updateStats() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('processed-count').textContent = data.processed;
                    document.getElementById('errors-count').textContent = data.errors;
                    if (data.last_processed) {
                        document.getElementById('last-processed').textContent = 
                            new Date(data.last_processed).toLocaleString();
                    }
                });
        }
        
        function updateSystemStats() {
            fetch('/api/system')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('cpu-usage').textContent = data.cpu + '%';
                    document.getElementById('cpu-bar').style.width = data.cpu + '%';
                    document.getElementById('memory-usage').textContent = data.memory + '%';
                    document.getElementById('memory-bar').style.width = data.memory + '%';
                    document.getElementById('disk-usage').textContent = data.disk + '%';
                    document.getElementById('disk-bar').style.width = data.disk + '%';
                });
        }
        
        function updateActivityLog() {
            fetch('/api/activity')
                .then(r => r.json())
                .then(data => {
                    const log = document.getElementById('activity-log');
                    log.innerHTML = data.logs.map(log => 
                        '<div class="log-entry">[' + log.time + '] ' + log.message + '</div>'
                    ).join('');
                    log.scrollTop = log.scrollHeight;
                });
        }
        
        function updateAPIs() {
            fetch('/api/external')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('api-status');
                    container.innerHTML = data.apis.map(api => 
                        '<div class="api-status ' + api.status + '">' +
                        '<strong>' + api.name + ':</strong> ' + api.message +
                        '</div>'
                    ).join('');
                });
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
            updateDashboard();
            updateInterval = setInterval(updateDashboard, 2000); // Update every 2 seconds
        };
        
        window.onbeforeunload = function() {
            if (updateInterval) clearInterval(updateInterval);
        };
    </script>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>📊 PDF Monitor Dashboard</h1>
            <p>Real-time monitoring and control panel</p>
        </div>
        
        <div class="widget-grid">
            <!-- Status Widget -->
            <div class="widget status-widget" id="status-widget">
                <div class="widget-header">
                    <div class="widget-title">Monitor Status</div>
                    <div class="widget-icon">📡</div>
                </div>
                <div id="status-text">Loading...</div>
                <div style="margin-top: 15px;">
                    <button class="btn btn-success" onclick="toggleMonitor()">Toggle</button>
                    <button class="btn" onclick="togglePause()">Pause/Resume</button>
                </div>
            </div>
            
            <!-- Statistics Widget -->
            <div class="widget">
                <div class="widget-header">
                    <div class="widget-title">Statistics</div>
                    <div class="widget-icon">📈</div>
                </div>
                <div class="stat-value" id="processed-count">0</div>
                <div class="stat-label">Files Processed</div>
                <div class="stat-value" id="errors-count">0</div>
                <div class="stat-label">Errors</div>
                <div style="margin-top: 10px; font-size: 12px; color: #666;">
                    Last: <span id="last-processed">Never</span>
                </div>
            </div>
            
            <!-- System Stats Widget -->
            <div class="widget">
                <div class="widget-header">
                    <div class="widget-title">System Resources</div>
                    <div class="widget-icon">💻</div>
                </div>
                <div class="system-stats">
                    <div>
                        <div style="font-size: 12px; color: #666;">CPU</div>
                        <div class="stat-value" id="cpu-usage" style="font-size: 24px;">0%</div>
                        <div class="progress-bar"><div class="progress-fill" id="cpu-bar" style="width: 0%"></div></div>
                    </div>
                    <div>
                        <div style="font-size: 12px; color: #666;">Memory</div>
                        <div class="stat-value" id="memory-usage" style="font-size: 24px;">0%</div>
                        <div class="progress-bar"><div class="progress-fill" id="memory-bar" style="width: 0%"></div></div>
                    </div>
                    <div>
                        <div style="font-size: 12px; color: #666;">Disk</div>
                        <div class="stat-value" id="disk-usage" style="font-size: 24px;">0%</div>
                        <div class="progress-bar"><div class="progress-fill" id="disk-bar" style="width: 0%"></div></div>
                    </div>
                </div>
            </div>
            
            <!-- Folders Widget -->
            <div class="widget">
                <div class="widget-header">
                    <div class="widget-title">Monitored Folders</div>
                    <div class="widget-icon">📁</div>
                </div>
                <div class="stat-value" id="folders-count" style="font-size: 32px;">0</div>
                <div class="stat-label">Active Folders</div>
                <div class="folder-list" id="folders-list"></div>
            </div>
            
            <!-- Activity Log Widget -->
            <div class="widget">
                <div class="widget-header">
                    <div class="widget-title">Activity Log</div>
                    <div class="widget-icon">📝</div>
                </div>
                <div class="log-widget" id="activity-log"></div>
            </div>
            
            <!-- API Status Widget -->
            <div class="widget api-widget">
                <div class="widget-header">
                    <div class="widget-title">External APIs</div>
                    <div class="widget-icon">🌐</div>
                </div>
                <div id="api-status">Loading API status...</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Activity log storage
activity_log = []

def log_activity(message):
    """Add entry to activity log"""
    activity_log.append({
        'time': datetime.now().strftime('%H:%M:%S'),
        'message': message
    })
    # Keep only last 50 entries
    if len(activity_log) > 50:
        activity_log.pop(0)

def init_monitor():
    global monitor
    if monitor is None:
        try:
            monitor = PDFMonitor()
            log_activity("Monitor initialized")
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
        'folders_count': len(monitor.config_manager.list_folders()) if monitor else 0
    })

@app.route('/api/stats')
def api_stats():
    return jsonify({
        'processed': stats.get('processed', 0),
        'errors': stats.get('errors', 0),
        'last_processed': stats.get('last_processed')
    })

@app.route('/api/system')
def api_system():
    """Get system resource usage"""
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        return jsonify({
            'cpu': round(cpu, 1),
            'memory': round(memory, 1),
            'disk': round(disk, 1)
        })
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        return jsonify({'cpu': 0, 'memory': 0, 'disk': 0})

@app.route('/api/activity')
def api_activity():
    """Get activity log"""
    return jsonify({'logs': activity_log[-20:]})  # Last 20 entries

@app.route('/api/external')
def api_external():
    """Check external API status - expandable for custom APIs"""
    apis = []
    
    # Example: Check if monitor is running
    try:
        if monitor and monitor.running:
            apis.append({
                'name': 'PDF Monitor',
                'status': 'success',
                'message': 'Running'
            })
        else:
            apis.append({
                'name': 'PDF Monitor',
                'status': 'error',
                'message': 'Stopped'
            })
    except:
        apis.append({
            'name': 'PDF Monitor',
            'status': 'error',
            'message': 'Not initialized'
        })
    
    # Add more API checks here
    # Example: Weather API, Calendar API, etc.
    
    return jsonify({'apis': apis})

@app.route('/api/folders')
def api_folders():
    if monitor is None:
        init_monitor()
    folders = monitor.config_manager.list_folders() if monitor else []
    return jsonify({'folders': folders})

@app.route('/api/toggle', methods=['POST'])
def api_toggle():
    if monitor is None:
        init_monitor()
    
    if not monitor:
        return jsonify({'message': 'Error: Monitor not initialized'}), 500
    
    if monitor.running:
        monitor.stop()
        log_activity("Monitor stopped")
        return jsonify({'message': 'Monitor stopped'})
    else:
        monitor.start()
        log_activity("Monitor started")
        return jsonify({'message': 'Monitor started'})

@app.route('/api/pause', methods=['POST'])
def api_pause():
    return jsonify({'message': 'Pause/resume not yet implemented in web interface'})

# API endpoint for adding custom data feeds
@app.route('/api/custom', methods=['GET', 'POST'])
def api_custom():
    """Custom API endpoint for external integrations"""
    if request.method == 'POST':
        data = request.get_json()
        # Process custom data here
        log_activity(f"Custom API call: {data}")
        return jsonify({'status': 'received', 'data': data})
    else:
        return jsonify({'message': 'Custom API endpoint', 'usage': 'POST JSON data here'})

def start_server(port=8888):
    time.sleep(2)
    try:
        webbrowser.open(f'http://127.0.0.1:{port}')
    except:
        print(f"Please open http://127.0.0.1:{port} in your browser")

if __name__ == '__main__':
    print("Starting PDF Monitor Enhanced Dashboard...")
    init_monitor()
    port = 8888
    print(f"Server starting at http://127.0.0.1:{port}")
    print("Opening browser...")
    threading.Thread(target=lambda: start_server(port), daemon=True).start()
    try:
        app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
    except OSError as e:
        if "Address already in use" in str(e):
            port = 8889
            print(f"Port 8888 is in use. Trying port {port}...")
            threading.Thread(target=lambda: time.sleep(2) or webbrowser.open(f'http://127.0.0.1:{port}'), daemon=True).start()
            app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
        else:
            raise

