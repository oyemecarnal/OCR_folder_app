# Dashboard Features & API Integration Guide

## Current Features

### Real-time Widgets
1. **Monitor Status** - Live ON/OFF status with toggle controls
2. **Statistics** - Files processed, errors, last processed time
3. **System Resources** - CPU, Memory, Disk usage with progress bars
4. **Monitored Folders** - List of active folders
5. **Activity Log** - Real-time processing log
6. **External APIs** - Status of connected APIs

### Auto-Updates
- All widgets update every 2 seconds automatically
- No page refresh needed
- Real-time data feeds

## Adding Custom APIs

### Method 1: Add to Existing Dashboard

Edit `pdf_monitor_dashboard.py` and modify the `api_external()` function:

```python
@app.route('/api/external')
def api_external():
    apis = []
    
    # Your custom API calls here
    from api_examples import APIIntegrations
    
    # Weather API
    weather = APIIntegrations.get_weather("YourCity", "YOUR_API_KEY")
    if weather['status'] == 'success':
        apis.append({
            'name': 'Weather',
            'status': 'success',
            'message': f"{weather['temperature']}°C"
        })
    
    # News API
    news = APIIntegrations.get_news_feed("YOUR_NEWS_API_KEY")
    if news['status'] == 'success':
        apis.append({
            'name': 'News',
            'status': 'success',
            'message': f"{news['total']} articles"
        })
    
    return jsonify({'apis': apis})
```

### Method 2: Create Custom Widget Endpoint

Add a new route for your custom data:

```python
@app.route('/api/custom-widget')
def api_custom_widget():
    # Fetch your data
    data = fetch_your_custom_data()
    return jsonify(data)
```

Then add to the HTML template:

```javascript
function updateCustomWidget() {
    fetch('/api/custom-widget')
        .then(r => r.json())
        .then(data => {
            // Update your widget
            document.getElementById('custom-widget').innerHTML = data.content;
        });
}
```

## Example API Integrations

### Weather API (OpenWeatherMap)
```python
# Get free API key from openweathermap.org
weather = APIIntegrations.get_weather("San Francisco", "YOUR_API_KEY")
```

### News API (NewsAPI.org)
```python
# Get free API key from newsapi.org
news = APIIntegrations.get_news_feed("YOUR_API_KEY", "technology")
```

### Stock Prices (Alpha Vantage)
```python
# Get free API key from alphavantage.co
stock = APIIntegrations.get_stock_price("AAPL", "YOUR_API_KEY")
```

### Custom REST API
```python
# Any REST API
result = APIIntegrations.get_custom_api(
    "https://api.example.com/data",
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)
```

## macOS Widget Integration

While you can't directly broadcast macOS widgets to Chrome, you can:

### Option 1: Create Web Widgets
- Design widgets in HTML/CSS/JavaScript
- Style them to look like macOS widgets
- Add to the dashboard

### Option 2: Use Chrome Homepage
1. Set dashboard as Chrome homepage:
   - Chrome Settings → On startup → Open a specific page
   - Add: `http://127.0.0.1:8888`

2. Create a new tab page:
   - Use Chrome extensions like "Momentum" or custom new tab
   - Embed your dashboard via iframe

### Option 3: Create Browser Extension
- Build a Chrome extension that shows your dashboard
- Can run as a popup or new tab page
- Access to Chrome APIs

## Adding New Widget Types

### Step 1: Add HTML Structure
In the HTML template, add a new widget:

```html
<div class="widget">
    <div class="widget-header">
        <div class="widget-title">My Custom Widget</div>
        <div class="widget-icon">🎯</div>
    </div>
    <div id="custom-widget-content">Loading...</div>
</div>
```

### Step 2: Add JavaScript Update Function
```javascript
function updateCustomWidget() {
    fetch('/api/my-custom-endpoint')
        .then(r => r.json())
        .then(data => {
            document.getElementById('custom-widget-content').innerHTML = 
                `<div>${data.content}</div>`;
        });
}
```

### Step 3: Add to Update Loop
```javascript
function updateDashboard() {
    updateStatus();
    updateStats();
    updateCustomWidget(); // Add here
    // ... other updates
}
```

### Step 4: Create API Endpoint
```python
@app.route('/api/my-custom-endpoint')
def api_custom():
    # Fetch your data
    return jsonify({
        'content': 'Your widget data here'
    })
```

## Live Data Feed Examples

### Real-time File Processing
Already implemented - shows live processing status

### System Monitoring
Already implemented - CPU, Memory, Disk

### Network Status
```python
@app.route('/api/network')
def api_network():
    import psutil
    net = psutil.net_io_counters()
    return jsonify({
        'bytes_sent': net.bytes_sent,
        'bytes_recv': net.bytes_recv,
        'packets_sent': net.packets_sent,
        'packets_recv': net.packets_recv
    })
```

### Calendar Events
```python
# Requires calendar API setup
@app.route('/api/calendar')
def api_calendar():
    # Fetch from Google Calendar, iCal, etc.
    events = fetch_calendar_events()
    return jsonify({'events': events})
```

## Making Dashboard Your Chrome Homepage

1. **Start the dashboard:**
   ```bash
   python3 pdf_monitor_dashboard.py
   ```

2. **Set as Chrome homepage:**
   - Open Chrome Settings
   - Go to "On startup"
   - Select "Open a specific page or set of pages"
   - Add: `http://127.0.0.1:8888`

3. **Or use as New Tab page:**
   - Install extension like "Custom New Tab"
   - Set URL to: `http://127.0.0.1:8888`

## Security Notes

- All APIs run locally (127.0.0.1)
- No external access by default
- API keys should be stored securely
- Use environment variables for sensitive data:
  ```python
  import os
  api_key = os.getenv('WEATHER_API_KEY')
  ```

## Next Steps

1. Add your API keys to environment variables
2. Customize widget styles
3. Add more data sources
4. Set dashboard as browser homepage
5. Create custom widgets for your needs

