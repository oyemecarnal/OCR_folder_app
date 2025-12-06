#!/usr/bin/env python3
"""
Simple launcher that ensures menu bar app shows up
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run
try:
    from pdf_monitor_app import main
    print("Starting PDF Monitor menu bar app...")
    print("Look for 'PDF Monitor' in your menu bar (top right)")
    print("If you don't see it, check the menu bar overflow area (arrow icon)")
    main()
except KeyboardInterrupt:
    print("\nShutting down...")
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)



