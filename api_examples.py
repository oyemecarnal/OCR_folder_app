#!/usr/bin/env python3
"""
Example API integrations for the dashboard
Shows how to add custom data feeds and external APIs
"""
import requests
import json
from datetime import datetime

class APIIntegrations:
    """Collection of API integration examples"""
    
    @staticmethod
    def get_weather(city="San Francisco", api_key=None):
        """Example: Weather API integration"""
        if not api_key:
            return {'status': 'error', 'message': 'API key required'}
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'success',
                    'temperature': round(data['main']['temp'] - 273.15, 1),  # Convert to Celsius
                    'description': data['weather'][0]['description'],
                    'city': city
                }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    @staticmethod
    def get_calendar_events(api_key=None):
        """Example: Google Calendar API integration"""
        # This would require OAuth setup
        return {'status': 'info', 'message': 'Calendar API requires OAuth setup'}
    
    @staticmethod
    def get_news_feed(api_key=None, category="technology"):
        """Example: News API integration"""
        if not api_key:
            return {'status': 'error', 'message': 'API key required'}
        
        try:
            url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={api_key}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'success',
                    'articles': data.get('articles', [])[:5],  # Top 5 articles
                    'total': data.get('totalResults', 0)
                }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    @staticmethod
    def get_stock_price(symbol="AAPL", api_key=None):
        """Example: Stock price API"""
        if not api_key:
            return {'status': 'error', 'message': 'API key required'}
        
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                quote = data.get('Global Quote', {})
                if quote:
                    return {
                        'status': 'success',
                        'symbol': symbol,
                        'price': quote.get('05. price'),
                        'change': quote.get('09. change')
                    }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    @staticmethod
    def get_custom_api(url, headers=None):
        """Generic API caller for custom endpoints"""
        try:
            response = requests.get(url, headers=headers or {}, timeout=5)
            if response.status_code == 200:
                return {
                    'status': 'success',
                    'data': response.json()
                }
            else:
                return {
                    'status': 'error',
                    'message': f'HTTP {response.status_code}'
                }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


# Example usage in dashboard:
# Add to pdf_monitor_dashboard.py in the api_external() function:
"""
from api_examples import APIIntegrations

# Add weather widget
weather = APIIntegrations.get_weather("San Francisco", "YOUR_API_KEY")
if weather['status'] == 'success':
    apis.append({
        'name': 'Weather',
        'status': 'success',
        'message': f"{weather['temperature']}°C - {weather['description']}"
    })

# Add news feed
news = APIIntegrations.get_news_feed("YOUR_NEWS_API_KEY")
if news['status'] == 'success':
    apis.append({
        'name': 'News',
        'status': 'success',
        'message': f"{news['total']} articles available"
    })
"""

