#!/usr/bin/env python3
"""
Test script to verify menu bar visibility
"""
import sys
import os

# Set up AppKit before importing rumps
try:
    import AppKit
    app = AppKit.NSApplication.sharedApplication()
    app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
    print("✓ Set activation policy to Accessory (menu bar only)")
except Exception as e:
    print(f"⚠ Could not set activation policy: {e}")

import rumps

class TestApp(rumps.App):
    def __init__(self):
        super(TestApp, self).__init__("🧪 TEST", icon=None)
        self.title = "🧪 TEST"
        self.menu = [
            rumps.MenuItem("Test Item", callback=self.test),
            rumps.MenuItem("Quit", callback=rumps.quit_application)
        ]
        print(f"✓ App initialized with title: {self.title}")
    
    def test(self, _):
        rumps.alert("Test", "Menu bar is working!", "OK")
        print("✓ Menu item clicked successfully")

if __name__ == '__main__':
    print("Starting test menu bar app...")
    print("Look for '🧪 TEST' in your menu bar")
    print("If you see it, rumps is working correctly")
    print("If not, there may be a macOS permission or space issue")
    print()
    
    try:
        app = TestApp()
        print("App created, starting event loop...")
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

