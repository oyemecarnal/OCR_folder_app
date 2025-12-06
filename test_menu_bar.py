#!/usr/bin/env python3
"""Quick test to verify menu bar app works"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import rumps
    print("✅ rumps is installed")
    
    # Quick test
    app = rumps.App("PDF Monitor Test", title="PDF Monitor")
    print("✅ Menu bar app can be created")
    print("\n📋 To see the menu bar icon:")
    print("   1. Look for 'PDF Monitor' text in your menu bar (top right)")
    print("   2. If you don't see it, check the overflow menu (arrow icon)")
    print("   3. The icon should appear when you run pdf_monitor_app.py")
    
except ImportError as e:
    print(f"❌ Error: {e}")
    print("   Install with: pip3 install rumps")
except Exception as e:
    print(f"❌ Error: {e}")
