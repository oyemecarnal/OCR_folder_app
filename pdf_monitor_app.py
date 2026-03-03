#!/usr/bin/env python3
"""
PDF Monitor Menu Bar App for macOS
"""
import os
import sys
import json
import threading
import time
from typing import List, Optional

# Hide dock icon - must be done before importing rumps
# This ensures the app runs as a menu bar-only app (no dock icon)
try:
    import AppKit
    # Set LSUIElement to hide dock icon but show menu bar
    bundle = AppKit.NSBundle.mainBundle()
    if bundle:
        info = bundle.infoDictionary()
        if info:
            info['LSUIElement'] = True
            info['LSBackgroundOnly'] = False  # We want menu bar, not pure background
    # Also set it on the application directly
    app = AppKit.NSApplication.sharedApplication()
    if app:
        app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
except Exception as e:
    print(f"Warning: Could not set AppKit properties: {e}")
    pass  # If AppKit not available, continue anyway

# Note: Output redirection is handled by the launcher script
# This allows the logger to work properly while still running silently

import rumps

# Import our monitor classes
from pdf_monitor import PDFMonitor, ConfigManager, logger

APP_NAME = "PDF Monitor"
CONFIG_FILE = 'monitored_folders.json'
STATS_FILE = 'monitor_stats.json'


class MonitorStats:
    """Track statistics for the monitor"""
    
    def __init__(self):
        self.stats_file = STATS_FILE
        self.stats = {
            'total_processed': 0,
            'total_errors': 0,
            'last_processed': None,
            'last_error': None
        }
        self.load()
    
    def load(self):
        """Load statistics from file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.stats.update(json.load(f))
            except Exception as e:
                logger.error(f"Error loading stats: {e}")
    
    def save(self):
        """Save statistics to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving stats: {e}")
    
    def increment_processed(self, filename: str = None):
        """Increment processed count"""
        self.stats['total_processed'] += 1
        if filename:
            self.stats['last_processed'] = filename
        self.save()
    
    def increment_errors(self, error: str = None):
        """Increment error count"""
        self.stats['total_errors'] += 1
        if error:
            self.stats['last_error'] = error
        self.save()
    
    def get_summary(self) -> str:
        """Get formatted summary"""
        return (f"Processed: {self.stats['total_processed']} | "
                f"Errors: {self.stats['total_errors']}")


class PDFMonitorApp(rumps.App):
    """Main menu bar application"""
    
    def __init__(self):
        try:
            # Initialize rumps app
            # When icon=None, rumps displays the name/title as text in menu bar
            # Use a short, visible name with emoji for better visibility
            super(PDFMonitorApp, self).__init__("📄 PDF Monitor", icon=None)
            # Set title property explicitly to ensure it shows
            self.title = "📄 PDF Monitor"
            logger.info(f"Menu bar app initialized with title: '{self.title}'")
            print(f"✓ Menu bar app initialized - Look for '{self.title}' in menu bar")
        except Exception as e:
            logger.error(f"Error initializing rumps app: {e}", exc_info=True)
            raise
        
        self.stats = MonitorStats()
        self.is_paused = False
        self.currently_processing = []
        self.processing_queue = []
        self.current_file = None
        self.progress_percent = 0
        
        try:
            # Create monitor with callbacks
            self.monitor = PDFMonitor(
                stats_callback=self.handle_stats_update,
                pause_check=lambda: self.is_paused,
                progress_callback=self.handle_progress_update
            )
            
            # Setup menu
            self.setup_menu()
            
            # Add default folder if needed
            if not self.monitor.config_manager.list_folders():
                default_folder = '/Users/kevinreed/Downloads/OCR'
                if os.path.isdir(default_folder):
                    self.monitor.config_manager.add_folder(default_folder)
            
            # Load monitoring state from config
            self.load_state()
            
            # Update menu periodically
            self.update_menu_timer = rumps.Timer(self.update_menu, 1)  # Update every second for progress
            self.update_menu_timer.start()
            
            # Initial title update (after menu is set up)
            self.update_title()
            
            # Initial folder menu build
            self.rebuild_folder_menu()
            
            logger.info("PDF Monitor app initialized successfully")
            print(f"✓ App fully initialized - Menu bar title: '{self.title}'")
            print(f"✓ If you don't see '{self.title}' in menu bar:")
            print(f"  1. Check the overflow area (>> icon on far right)")
            print(f"  2. Try: killall SystemUIServer")
            print(f"  3. Check menu bar space - it may be hidden if menu bar is full")
            
            # Show notification that app is running
            try:
                rumps.notification(
                    APP_NAME, 
                    "PDF Monitor is running", 
                    f"Look for '{self.title}' in menu bar (top right)"
                )
            except:
                pass
        except Exception as e:
            logger.error(f"Error during app setup: {e}", exc_info=True)
            raise
    
    def handle_stats_update(self, event_type: str, data: str):
        """Handle statistics updates from monitor"""
        if event_type == 'processed':
            self.stats.increment_processed(data)
        elif event_type == 'error':
            self.stats.increment_errors(data)
    
    def handle_progress_update(self, event_type: str, data: str):
        """Handle progress updates from monitor"""
        if event_type == 'queued':
            if data not in self.processing_queue:
                self.processing_queue.append(data)
        elif event_type == 'started':
            self.current_file = data
            if data in self.processing_queue:
                self.processing_queue.remove(data)
        elif event_type == 'completed':
            if data in self.processing_queue:
                self.processing_queue.remove(data)
            if self.current_file == data:
                self.current_file = None
                self.progress_percent = 0
        # Update title with progress info
        self.update_title()
    
    def setup_menu(self):
        """Setup the menu bar menu"""
        try:
            self.menu = [
                rumps.MenuItem("Monitor ON", callback=self.toggle_monitor),
                rumps.separator,
                rumps.MenuItem("Folders", callback=None),
                rumps.separator,
                rumps.MenuItem("Process Files...", callback=None),
                rumps.MenuItem("  Select Files...", callback=self.select_files_for_ocr),
                rumps.MenuItem("  Process All in Folders", callback=self.process_all_files),
                rumps.MenuItem("  Process Recent (<1 day)", callback=self.process_recent_files),
                rumps.separator,
                rumps.MenuItem("Pause", callback=self.toggle_pause),
                rumps.MenuItem("Statistics", callback=self.show_stats),
                rumps.MenuItem("Preferences...", callback=self.show_preferences),
                rumps.separator,
                rumps.MenuItem("Quit", callback=self.quit_app)
            ]
            
            # Initialize monitor state
            self.menu["Monitor ON"].state = 0
            self.menu["Pause"].state = 0
            logger.info("Menu setup completed")
        except Exception as e:
            logger.error(f"Error setting up menu: {e}", exc_info=True)
            raise
    
    def load_state(self):
        """Load saved monitoring state"""
        try:
            config = self.monitor.config_manager
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    enabled = data.get('monitor_enabled', False)
                    if enabled and config.list_folders():
                        self.start_monitoring()
        except Exception as e:
            logger.error(f"Error loading state: {e}")
    
    def save_state(self):
        """Save monitoring state"""
        try:
            config = self.monitor.config_manager
            data = {
                'folders': config.list_folders(),
                'monitor_enabled': self.monitor.running and not self.is_paused
            }
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving state: {e}")
    
    def update_title(self):
        """Update menu bar title with progress info"""
        # Get queue info from handler
        handler_queue = getattr(self.monitor.handler, 'processing_queue', [])
        current_file = getattr(self.monitor.handler, 'current_file', None)
        
        total_files = len(handler_queue) + (1 if current_file else 0)
        
        if total_files > 0:
            if current_file:
                # Show progress: files remaining
                remaining = len(handler_queue)
                if remaining > 0:
                    self.title = f"📄 PDF Monitor ({remaining + 1} files)"
                else:
                    self.title = "📄 PDF Monitor (Processing...)"
            else:
                self.title = f"📄 PDF Monitor ({len(handler_queue)} queued)"
        else:
            if self.monitor.running and not self.is_paused:
                self.title = "📄 PDF Monitor"
            else:
                self.title = "📄 PDF Monitor (OFF)"
    
    def update_menu(self, _):
        """Update menu with current folders and status"""
        folders = self.monitor.config_manager.list_folders()
        
        # Check if folder count changed and rebuild if needed
        current_count = len(folders)
        if not hasattr(self, '_last_folder_count') or self._last_folder_count != current_count:
            self._last_folder_count = current_count
            self.rebuild_folder_menu()
        
        # Update monitor status menu title
        if self.monitor.running and not self.is_paused:
            if "Monitor ON" in self.menu:
                self.menu["Monitor ON"].title = "Monitor ON"
                self.menu["Monitor ON"].state = 1
        else:
            if "Monitor ON" in self.menu:
                self.menu["Monitor ON"].title = "Monitor OFF"
                self.menu["Monitor ON"].state = 0
        
        # Update pause status
        if "Pause" in self.menu:
            if self.is_paused:
                self.menu["Pause"].title = "Resume"
                self.menu["Pause"].state = 1
            else:
                self.menu["Pause"].title = "Pause"
                self.menu["Pause"].state = 0
        
        # Update title with progress
        self.update_title()
    
    def rebuild_folder_menu(self):
        """Rebuild the folder menu section"""
        folders = self.monitor.config_manager.list_folders()
        
        # Remove existing folder items
        items_to_remove = []
        for key in list(self.menu.keys()):
            if isinstance(key, str):
                if key.startswith(("1. ", "2. ", "3. ", "4. ", "5. ")) or \
                   key in ["Manage All Folders...", "Add Folder..."]:
                    items_to_remove.append(key)
        
        for key in items_to_remove:
            if key in self.menu:
                del self.menu[key]
        
        # Add folder items
        for i, folder in enumerate(folders[:4]):
            # Create a shorter display name
            display_name = os.path.basename(folder) if os.path.basename(folder) else folder
            if len(folder) > 50:
                # Show first part and last part
                display_name = folder[:20] + "..." + folder[-27:]
            
            item = rumps.MenuItem(
                f"{i+1}. {display_name}",
                callback=lambda _, f=folder: self.open_folder(f)
            )
            self.menu.insert_after("Folders", item)
        
        # Add separator and manage option
        if len(folders) >= 4:
            self.menu.insert_after("Folders", rumps.separator)
            manage_item = rumps.MenuItem("5. Manage All Folders...", callback=self.show_preferences)
            self.menu.insert_after("Folders", manage_item)
        elif len(folders) > 0:
            self.menu.insert_after("Folders", rumps.separator)
            add_item = rumps.MenuItem("Add Folder...", callback=self.show_preferences)
            self.menu.insert_after("Folders", add_item)
        
        # Track folder count
        if not hasattr(self, '_last_folder_count'):
            self._last_folder_count = len(folders)
    
    def toggle_monitor(self, sender):
        """Toggle monitoring on/off"""
        if self.monitor.running and not self.is_paused:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def start_monitoring(self):
        """Start monitoring"""
        if self.is_paused:
            self.is_paused = False
            rumps.notification(APP_NAME, "Monitor Resumed", "PDF monitoring has been resumed")
            return
        
        if not self.monitor.config_manager.list_folders():
            rumps.alert(
                "No Folders Configured",
                "Please add at least one folder to monitor in Preferences.",
                "OK"
            )
            return
        
        try:
            self.monitor.start()
            self.save_state()
            rumps.notification(APP_NAME, "Monitor Started", f"Monitoring {len(self.monitor.observers)} folder(s)")
        except Exception as e:
            logger.error(f"Error starting monitor: {e}")
            rumps.alert("Error", f"Failed to start monitoring: {e}", "OK")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        try:
            self.monitor.stop()
            self.save_state()
            rumps.notification(APP_NAME, "Monitor Stopped", "PDF monitoring has been stopped")
        except Exception as e:
            logger.error(f"Error stopping monitor: {e}")
    
    def toggle_pause(self, sender):
        """Pause/resume monitoring"""
        if not self.monitor.running:
            rumps.alert("Monitor Not Running", "Please start monitoring first.", "OK")
            return
        
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            # Don't actually stop observers, just prevent processing
            rumps.notification(APP_NAME, "Monitor Paused", "Monitoring is paused - no files will be processed")
        else:
            rumps.notification(APP_NAME, "Monitor Resumed", "Monitoring has been resumed")
        
        self.save_state()
    
    def open_folder(self, folder_path: str):
        """Open folder in Finder"""
        try:
            os.system(f'open "{folder_path}"')
        except Exception as e:
            logger.error(f"Error opening folder: {e}")
            rumps.alert("Error", f"Failed to open folder: {e}", "OK")
    
    def show_stats(self, sender):
        """Show statistics window"""
        stats_text = f"""
Statistics:

Total Processed: {self.stats.stats['total_processed']}
Total Errors: {self.stats.stats['total_errors']}
Last Processed: {self.stats.stats['last_processed'] or 'None'}
Folders Monitored: {len(self.monitor.config_manager.list_folders())}
Status: {'Running' if (self.monitor.running and not self.is_paused) else 'Stopped/Paused'}
        """.strip()
        
        rumps.alert("PDF Monitor Statistics", stats_text, "OK")
    
    def show_preferences(self, sender=None):
        """Show preferences window for managing folders"""
        # Create preferences window in a separate thread
        threading.Thread(target=self._show_preferences_window, daemon=True).start()
    
    def _show_preferences_window(self):
        """Open preferences window using tkinter"""
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox
        
        class PreferencesWindow:
            def __init__(self, app):
                self.app = app
                self.root = tk.Tk()
                self.root.title("PDF Monitor Preferences")
                self.root.geometry("600x500")
                self.root.resizable(True, True)
                
                # Make window appear on top
                self.root.lift()
                self.root.attributes('-topmost', True)
                self.root.after_idle(lambda: self.root.attributes('-topmost', False))
                
                self.setup_ui()
                self.update_folder_list()
                
                # Center window
                self.center_window()
            
            def center_window(self):
                """Center window on screen"""
                self.root.update_idletasks()
                width = self.root.winfo_width()
                height = self.root.winfo_height()
                x = (self.root.winfo_screenwidth() // 2) - (width // 2)
                y = (self.root.winfo_screenheight() // 2) - (height // 2)
                self.root.geometry(f'{width}x{height}+{x}+{y}')
            
            def setup_ui(self):
                """Setup the UI"""
                # Title
                title_frame = ttk.Frame(self.root, padding="10")
                title_frame.pack(fill=tk.X)
                ttk.Label(title_frame, text="PDF Monitor Preferences", 
                         font=("Helvetica", 16, "bold")).pack()
                
                # Folder list frame
                list_frame = ttk.LabelFrame(self.root, text="Monitored Folders", padding="10")
                list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Listbox with scrollbar
                scrollbar = ttk.Scrollbar(list_frame)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                self.listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, 
                                         font=("Menlo", 11))
                self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.config(command=self.listbox.yview)
                
                # Button frame
                button_frame = ttk.Frame(self.root, padding="10")
                button_frame.pack(fill=tk.X)
                
                ttk.Button(button_frame, text="Add Folder...", 
                          command=self.add_folder).pack(side=tk.LEFT, padx=5)
                ttk.Button(button_frame, text="Remove Selected", 
                          command=self.remove_folder).pack(side=tk.LEFT, padx=5)
                ttk.Button(button_frame, text="Refresh", 
                          command=self.update_folder_list).pack(side=tk.LEFT, padx=5)
                
                # Close button
                close_frame = ttk.Frame(self.root, padding="10")
                close_frame.pack(fill=tk.X)
                ttk.Button(close_frame, text="Close", 
                          command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
            
            def update_folder_list(self):
                """Update the folder list display"""
                self.listbox.delete(0, tk.END)
                folders = self.app.monitor.config_manager.list_folders()
                for folder in folders:
                    self.listbox.insert(tk.END, folder)
            
            def add_folder(self):
                """Add a new folder"""
                folder = filedialog.askdirectory(title="Select Folder to Monitor")
                if folder:
                    if self.app.monitor.config_manager.add_folder(folder):
                        # Restart monitor if running
                        was_running = self.app.monitor.running
                        if was_running:
                            self.app.monitor.stop()
                        self.update_folder_list()
                        if was_running:
                            self.app.monitor.start()
                        self.app.rebuild_folder_menu()
                        self.app.save_state()
                        messagebox.showinfo("Success", f"Added folder: {folder}")
                    else:
                        messagebox.showerror("Error", f"Failed to add folder: {folder}")
            
            def remove_folder(self):
                """Remove selected folder"""
                selection = self.listbox.curselection()
                if not selection:
                    messagebox.showwarning("No Selection", "Please select a folder to remove")
                    return
                
                index = selection[0]
                folders = self.app.monitor.config_manager.list_folders()
                if 0 <= index < len(folders):
                    folder = folders[index]
                    if messagebox.askyesno("Confirm", f"Remove folder from monitoring?\n\n{folder}"):
                        if self.app.monitor.config_manager.remove_folder(folder):
                            # Restart monitor if running
                            was_running = self.app.monitor.running
                            if was_running:
                                self.app.monitor.stop()
                            self.update_folder_list()
                            if was_running:
                                self.app.monitor.start()
                            self.app.rebuild_folder_menu()
                            self.app.save_state()
                            messagebox.showinfo("Success", f"Removed folder: {folder}")
                        else:
                            messagebox.showerror("Error", f"Failed to remove folder: {folder}")
        
        try:
            window = PreferencesWindow(self)
            window.root.mainloop()
        except Exception as e:
            logger.error(f"Error showing preferences: {e}")
            rumps.alert("Error", f"Failed to open preferences: {e}", "OK")
    
    def select_files_for_ocr(self, sender):
        """Open file selection dialog to choose PDFs for OCR"""
        import tkinter as tk
        from tkinter import filedialog
        
        def select_and_process():
            root = tk.Tk()
            root.withdraw()  # Hide main window
            root.lift()
            root.attributes('-topmost', True)
            
            files = filedialog.askopenfilenames(
                title="Select PDF files to process with OCR",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            root.destroy()
            
            if files:
                self.process_files_list(list(files))
        
        threading.Thread(target=select_and_process, daemon=True).start()
    
    def process_all_files(self, sender):
        """Process all PDF files in monitored folders"""
        folders = self.monitor.config_manager.list_folders()
        if not folders:
            rumps.alert("No Folders", "Please add folders in Preferences first.", "OK")
            return
        
        if rumps.alert(
            "Process All Files?",
            f"This will process all PDF files in {len(folders)} monitored folder(s).\n\nThis may take a while. Continue?",
            "Process All",
            "Cancel"
        ) == 1:  # Process All button
            threading.Thread(target=self._process_all_files_thread, daemon=True).start()
    
    def process_recent_files(self, sender):
        """Process PDF files modified in the last 24 hours"""
        folders = self.monitor.config_manager.list_folders()
        if not folders:
            rumps.alert("No Folders", "Please add folders in Preferences first.", "OK")
            return
        
        if rumps.alert(
            "Process Recent Files?",
            f"This will process PDF files modified in the last 24 hours in {len(folders)} monitored folder(s).\n\nContinue?",
            "Process Recent",
            "Cancel"
        ) == 1:  # Process Recent button
            threading.Thread(target=self._process_recent_files_thread, daemon=True).start()
    
    def _process_all_files_thread(self):
        """Thread to process all files"""
        folders = self.monitor.config_manager.list_folders()
        all_files = []
        
        for folder in folders:
            if os.path.isdir(folder):
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        if file.lower().endswith('.pdf'):
                            filepath = os.path.join(root, file)
                            all_files.append(filepath)
        
        if all_files:
            rumps.notification(APP_NAME, "Processing Started", f"Found {len(all_files)} PDF file(s) to process")
            self.process_files_list(all_files)
        else:
            rumps.notification(APP_NAME, "No Files Found", "No PDF files found in monitored folders")
    
    def _process_recent_files_thread(self):
        """Thread to process recent files"""
        folders = self.monitor.config_manager.list_folders()
        cutoff_time = time.time() - (24 * 60 * 60)  # 24 hours ago
        recent_files = []
        
        for folder in folders:
            if os.path.isdir(folder):
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        if file.lower().endswith('.pdf'):
                            filepath = os.path.join(root, file)
                            try:
                                mtime = os.path.getmtime(filepath)
                                if mtime >= cutoff_time:
                                    recent_files.append(filepath)
                            except:
                                pass
        
        if recent_files:
            rumps.notification(APP_NAME, "Processing Started", f"Found {len(recent_files)} recent PDF file(s) to process")
            self.process_files_list(recent_files)
        else:
            rumps.notification(APP_NAME, "No Recent Files", "No PDF files modified in the last 24 hours")
    
    def process_files_list(self, filepaths: List[str]):
        """Process a list of PDF files"""
        processed_count = 0
        error_count = 0
        skipped_count = 0
        
        for filepath in filepaths:
            try:
                # Validate file exists
                if not os.path.exists(filepath):
                    logger.warning(f"File not found: {filepath}")
                    continue
                
                # Check if already processed
                if hasattr(self.monitor.handler, 'processed_files') and filepath in self.monitor.handler.processed_files:
                    logger.info(f"Skipping already processed: {filepath}")
                    skipped_count += 1
                    continue
                
                # Process the file using the handler's process_pdf method
                self.monitor.handler.process_pdf(filepath, self.handle_progress_update)
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing {filepath}: {e}")
                error_count += 1
                if self.stats:
                    self.stats.increment_errors(str(e))
        
        # Show completion notification
        message = f"Processed: {processed_count}"
        if skipped_count > 0:
            message += f", Skipped: {skipped_count}"
        if error_count > 0:
            message += f", Errors: {error_count}"
        
        rumps.notification(
            APP_NAME,
            "Processing Complete",
            message
        )
    
    def quit_app(self, sender):
        """Quit application"""
        if rumps.alert(
            "Quit PDF Monitor?",
            "Are you sure you want to quit? Monitoring will stop.",
            "Quit",
            "Cancel"
        ) == 1:  # 1 = Quit button
            self.stop_monitoring()
            self.save_state()
            rumps.quit_application()


def main():
    """Main entry point"""
    # Check if we're on macOS
    if sys.platform != 'darwin':
        print("This app is designed for macOS only")
        sys.exit(1)
    
    try:
        print("Starting PDF Monitor menu bar app...")
        print("Look for 'PDF Monitor' in your menu bar (top right corner)")
        app = PDFMonitorApp()
        print("App initialized, starting event loop...")
        print("App is now running. Check your menu bar for 'PDF Monitor'")
        logger.info("Starting app.run()...")
        app.run()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
        print("\nShutting down...")
    except Exception as e:
        logger.error(f"Error starting app: {e}", exc_info=True)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

