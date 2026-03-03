#!/usr/bin/env python3
"""
Menu Bar Widget for PDF Monitor
Shows status in menu bar and opens control panel when clicked
"""

import rumps
import json
import os
from pathlib import Path

class PDFMonitorMenuBar(rumps.App):
    def __init__(self):
        super(PDFMonitorMenuBar, self).__init__("📄 PDF Monitor", icon=None, title="📄")
        self.config_file = Path(__file__).parent / 'widget_config.json'
        self.load_config()
        self.setup_menu()
        
        # Update timer
        self.update_timer = rumps.Timer(self.update_status, 10)  # Update every 10 seconds
        self.update_timer.start()
        self.update_status(None)
    
    def load_config(self):
        """Load configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = {'monitoring': False, 'folder': '', 'max_age_hours': 1}
        else:
            self.config = {'monitoring': False, 'folder': '', 'max_age_hours': 1}
    
    def setup_menu(self):
        """Setup menu bar menu"""
        self.menu = [
            rumps.MenuItem("Status: OFF", callback=None),
            rumps.separator,
            rumps.MenuItem("Toggle Monitoring", callback=self.toggle_monitoring),
            rumps.MenuItem("Select Folder...", callback=self.select_folder),
            rumps.MenuItem("Open Widget Window", callback=self.open_widget),
            rumps.separator,
            rumps.MenuItem("Quit", callback=rumps.quit_application)
        ]
    
    def update_status(self, _):
        """Update menu bar status"""
        self.load_config()
        status = "ON" if self.config.get('monitoring', False) else "OFF"
        color = "🟢" if status == "ON" else "🔴"
        
        # Update title
        self.title = f"📄 {color}"
        
        # Update menu
        if "Status: " in self.menu:
            self.menu["Status: OFF"].title = f"Status: {status} {color}"
        
        # Update toggle button
        if "Toggle Monitoring" in self.menu:
            self.menu["Toggle Monitoring"].title = "Stop Monitoring" if status == "ON" else "Start Monitoring"
    
    def toggle_monitoring(self, sender):
        """Toggle monitoring"""
        self.load_config()
        self.config['monitoring'] = not self.config.get('monitoring', False)
        
        # Save config
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        
        status = "started" if self.config['monitoring'] else "stopped"
        rumps.notification("PDF Monitor", f"Monitoring {status}", 
                          f"Folder: {self.config.get('folder', 'None')}")
        self.update_status(None)
    
    def select_folder(self, sender):
        """Open folder selection in widget window"""
        # Launch the widget window
        import subprocess
        widget_path = Path(__file__).parent / 'pdf_monitor_widget.py'
        subprocess.Popen(['python3', str(widget_path)])
        rumps.notification("PDF Monitor", "Widget Window", "Opening widget window to select folder...")
    
    def open_widget(self, sender):
        """Open the widget window"""
        import subprocess
        widget_path = Path(__file__).parent / 'pdf_monitor_widget.py'
        subprocess.Popen(['python3', str(widget_path)])
    
    @rumps.clicked("Status: OFF")
    def show_status(self, sender):
        """Show status info"""
        self.load_config()
        folder = self.config.get('folder', 'No folder selected')
        status = "ON" if self.config.get('monitoring', False) else "OFF"
        rumps.alert("PDF Monitor Status", 
                   f"Status: {status}\nFolder: {folder}\nAge: {self.config.get('max_age_hours', 1)} hours",
                   "OK")

if __name__ == '__main__':
    app = PDFMonitorMenuBar()
    app.run()

