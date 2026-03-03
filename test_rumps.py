#!/usr/bin/env python3
"""Test script to verify rumps works"""
import rumps
import sys

class TestApp(rumps.App):
    def __init__(self):
        super(TestApp, self).__init__("Test")
        self.menu = [rumps.MenuItem("Test Item", callback=self.test_callback)]
    
    def test_callback(self, _):
        rumps.alert("Test", "Rumps is working!", "OK")

if __name__ == '__main__':
    print("Testing rumps...")
    try:
        app = TestApp()
        print("App created successfully, starting...")
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)



