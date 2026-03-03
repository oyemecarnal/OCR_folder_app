#!/usr/bin/env python3
"""
Native macOS Widget App for PDF Monitor
Uses tkinter for native macOS window
"""

import tkinter as tk
from tkinter import ttk
import json
import threading
import time
from urllib.request import urlopen, Request
from urllib.error import URLError

class PDFMonitorWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Monitor Widget")
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # State
        self.status = "off"
        self.processed = 0
        self.errors = 0
        self.server_url = "http://localhost:5002"
        
        # Setup UI
        self.setup_ui()
        
        # Start auto-refresh
        self.refresh_status()
        self.root.after(10000, self.auto_refresh)  # Refresh every 10 seconds
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup the widget UI"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status indicator
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(pady=20)
        
        self.status_canvas = tk.Canvas(status_frame, width=100, height=100, highlightthickness=0)
        self.status_canvas.pack()
        self.status_circle = self.status_canvas.create_oval(10, 10, 90, 90, width=3, outline="")
        
        # Status text
        self.status_label = ttk.Label(main_frame, text="OFF", font=("SF Pro Display", 32, "bold"))
        self.status_label.pack(pady=5)
        
        ttk.Label(main_frame, text="PDF Monitor", font=("SF Pro Display", 12)).pack()
        
        # Statistics
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(pady=20, fill=tk.X)
        
        # Processed
        processed_frame = ttk.Frame(stats_frame)
        processed_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        ttk.Label(processed_frame, text="0", font=("SF Pro Display", 24, "bold"), foreground="red").pack()
        ttk.Label(processed_frame, text="Processed", font=("SF Pro Display", 10)).pack()
        self.processed_label = processed_frame.children['!label']
        
        # Errors
        errors_frame = ttk.Frame(stats_frame)
        errors_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        ttk.Label(errors_frame, text="0", font=("SF Pro Display", 24, "bold"), foreground="red").pack()
        ttk.Label(errors_frame, text="Errors", font=("SF Pro Display", 10)).pack()
        self.errors_label = errors_frame.children['!label']
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        self.toggle_btn = ttk.Button(button_frame, text="Toggle", command=self.toggle_monitor, width=15)
        self.toggle_btn.pack(pady=5)
        
        self.onoff_btn = ttk.Button(button_frame, text="Turn ON", command=self.turn_on_off, width=15)
        self.onoff_btn.pack(pady=5)
        
        # Status message
        self.message_label = ttk.Label(main_frame, text="", font=("SF Pro Display", 9), foreground="gray")
        self.message_label.pack(pady=10)
    
    def update_status_display(self):
        """Update the visual status display"""
        color = "#34C759" if self.status == "on" else "#FF3B30"
        symbol = "✓" if self.status == "on" else "○"
        
        # Update circle
        self.status_canvas.delete(self.status_circle)
        self.status_circle = self.status_canvas.create_oval(
            10, 10, 90, 90, 
            width=3, 
            outline=color,
            fill=color + "20"  # Semi-transparent fill
        )
        
        # Update text
        self.status_label.config(text=self.status.upper(), foreground=color)
        self.processed_label.config(text=str(self.processed), foreground=color)
        self.errors_label.config(text=str(self.errors))
        
        # Update button
        self.onoff_btn.config(text="Turn OFF" if self.status == "on" else "Turn ON")
        self.toggle_btn.config(style="Accent.TButton" if self.status == "on" else "TButton")
    
    def refresh_status(self):
        """Fetch status from server"""
        def fetch():
            try:
                url = f"{self.server_url}/api/status"
                req = Request(url)
                with urlopen(req, timeout=2) as response:
                    data = json.loads(response.read().decode())
                    self.status = data.get('status', 'off')
                    stats = data.get('stats', {})
                    self.processed = stats.get('processed', 0)
                    self.errors = stats.get('errors', 0)
                    self.root.after(0, self.update_status_display)
                    self.root.after(0, lambda: self.message_label.config(text=""))
            except URLError:
                self.root.after(0, lambda: self.message_label.config(
                    text="⚠️ Server not running", foreground="orange"
                ))
            except Exception as e:
                self.root.after(0, lambda: self.message_label.config(
                    text=f"Error: {str(e)[:30]}", foreground="red"
                ))
        
        threading.Thread(target=fetch, daemon=True).start()
    
    def auto_refresh(self):
        """Auto-refresh status"""
        self.refresh_status()
        self.root.after(10000, self.auto_refresh)  # Schedule next refresh
    
    def toggle_monitor(self):
        """Toggle monitor on/off"""
        self.send_command("/api/toggle")
    
    def turn_on_off(self):
        """Turn monitor on or off"""
        endpoint = "/api/off" if self.status == "on" else "/api/on"
        self.send_command(endpoint)
    
    def send_command(self, endpoint):
        """Send command to server"""
        def send():
            try:
                url = f"{self.server_url}{endpoint}"
                req = Request(url, method="POST")
                with urlopen(req, timeout=2) as response:
                    data = json.loads(response.read().decode())
                    self.root.after(0, lambda: self.message_label.config(
                        text="✓ " + data.get('message', 'Success'), foreground="green"
                    ))
                    time.sleep(0.5)
                    self.refresh_status()
            except Exception as e:
                self.root.after(0, lambda: self.message_label.config(
                    text=f"Error: {str(e)[:30]}", foreground="red"
                ))
        
        threading.Thread(target=send, daemon=True).start()


def main():
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('aqua')  # macOS native theme
    
    app = PDFMonitorWidget(root)
    root.mainloop()


if __name__ == '__main__':
    main()

