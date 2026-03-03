#!/usr/bin/env python3
"""
Simple PDF Monitor macOS Widget
- Toggle ON/OFF
- Select folder to monitor
- Process files < 1 hour old (customizable)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import time
import threading
from pathlib import Path
import subprocess

class PDFMonitorWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Monitor")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Config file
        self.config_file = Path(__file__).parent / 'widget_config.json'
        self.load_config()
        
        # State
        self.monitoring = False
        self.monitor_thread = None
        
        # Setup UI
        self.setup_ui()
        
        # Update status
        self.update_display()
    
    def load_config(self):
        """Load configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = {}
        else:
            self.config = {
                'folder': '',
                'max_age_hours': 1,
                'monitoring': False
            }
        self.save_config()
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_ui(self):
        """Setup the widget UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="PDF Monitor", font=("SF Pro Display", 18, "bold"))
        title.pack(pady=10)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(pady=10, fill=tk.X)
        
        self.status_label = ttk.Label(status_frame, text="OFF", font=("SF Pro Display", 14, "bold"), foreground="red")
        self.status_label.pack()
        
        # Folder selection
        folder_frame = ttk.LabelFrame(main_frame, text="Monitor Folder", padding="10")
        folder_frame.pack(pady=10, fill=tk.X)
        
        self.folder_label = ttk.Label(folder_frame, text=self.config.get('folder', 'No folder selected'), 
                                      wraplength=350, foreground="gray")
        self.folder_label.pack(pady=5)
        
        ttk.Button(folder_frame, text="Select Folder", command=self.select_folder).pack()
        
        # Settings
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.pack(pady=10, fill=tk.X)
        
        age_frame = ttk.Frame(settings_frame)
        age_frame.pack(fill=tk.X)
        
        ttk.Label(age_frame, text="Process files newer than:").pack(side=tk.LEFT)
        self.age_var = tk.StringVar(value=str(self.config.get('max_age_hours', 1)))
        age_spin = ttk.Spinbox(age_frame, from_=0.1, to=24, increment=0.1, width=10, textvariable=self.age_var,
                              command=self.save_age_setting)
        age_spin.pack(side=tk.RIGHT)
        ttk.Label(age_frame, text="hours").pack(side=tk.RIGHT, padx=5)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        self.toggle_btn = ttk.Button(button_frame, text="Start Monitoring", command=self.toggle_monitoring,
                                     width=20)
        self.toggle_btn.pack(pady=5)
        
        ttk.Button(button_frame, text="Process Now", command=self.process_now, width=20).pack(pady=5)
    
    def save_age_setting(self):
        """Save age setting"""
        try:
            self.config['max_age_hours'] = float(self.age_var.get())
            self.save_config()
        except:
            pass
    
    def select_folder(self):
        """Select folder to monitor"""
        folder = filedialog.askdirectory(title="Select Folder to Monitor for PDFs")
        if folder:
            self.config['folder'] = folder
            self.save_config()
            self.folder_label.config(text=folder, foreground="black")
            messagebox.showinfo("Folder Selected", f"Monitoring: {folder}")
    
    def update_display(self):
        """Update the display"""
        if self.monitoring:
            self.status_label.config(text="ON", foreground="green")
            self.toggle_btn.config(text="Stop Monitoring")
        else:
            self.status_label.config(text="OFF", foreground="red")
            self.toggle_btn.config(text="Start Monitoring")
    
    def toggle_monitoring(self):
        """Toggle monitoring on/off"""
        if not self.config.get('folder'):
            messagebox.showwarning("No Folder", "Please select a folder first")
            return
        
        if not os.path.isdir(self.config['folder']):
            messagebox.showerror("Invalid Folder", "Selected folder does not exist")
            return
        
        self.monitoring = not self.monitoring
        self.config['monitoring'] = self.monitoring
        self.save_config()
        
        if self.monitoring:
            self.start_monitoring()
        else:
            self.stop_monitoring()
        
        self.update_display()
    
    def start_monitoring(self):
        """Start monitoring folder"""
        if self.monitor_thread and self.monitor_thread.is_alive():
            return
        
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        messagebox.showinfo("Monitoring Started", f"Monitoring: {self.config['folder']}\n\nFiles newer than {self.config.get('max_age_hours', 1)} hours will be processed.")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        messagebox.showinfo("Monitoring Stopped", "Monitoring has been stopped.")
    
    def monitor_loop(self):
        """Monitor folder for new files"""
        folder = self.config['folder']
        max_age_seconds = self.config.get('max_age_hours', 1) * 3600
        
        processed_files = set()
        processed_file = Path(__file__).parent / 'processed_files_widget.txt'
        
        # Load already processed files
        if processed_file.exists():
            with open(processed_file, 'r') as f:
                processed_files = set(line.strip() for line in f if line.strip())
        
        while self.monitoring:
            try:
                # Scan folder for PDFs
                for file_path in Path(folder).glob("*.pdf"):
                    file_str = str(file_path)
                    
                    # Skip if already processed
                    if file_str in processed_files:
                        continue
                    
                    # Check file age
                    try:
                        file_age = time.time() - file_path.stat().st_mtime
                        if file_age <= max_age_seconds:
                            # Process this file
                            self.process_pdf(file_path)
                            processed_files.add(file_str)
                            
                            # Save processed file
                            with open(processed_file, 'a') as f:
                                f.write(f"{file_str}\n")
                    except Exception as e:
                        print(f"Error checking {file_path}: {e}")
                
                # Check every 30 seconds
                time.sleep(30)
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(30)
    
    def process_pdf(self, file_path):
        """Process a PDF file with OCR"""
        try:
            print(f"Processing: {file_path}")
            # Use ocrmypdf to process
            temp_file = str(file_path) + ".ocr_temp"
            
            import ocrmypdf
            ocrmypdf.ocr(
                str(file_path),
                temp_file,
                language='eng',
                progress_bar=False,
                optimize=1,
                force_ocr=False,
            )
            
            # Replace original
            os.replace(temp_file, str(file_path))
            print(f"✓ Processed: {file_path}")
            
            # Show notification
            self.root.after(0, lambda: messagebox.showinfo("PDF Processed", f"OCR completed:\n{file_path.name}"))
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to process:\n{file_path.name}\n\n{str(e)}"))
    
    def process_now(self):
        """Process files in folder now"""
        if not self.config.get('folder'):
            messagebox.showwarning("No Folder", "Please select a folder first")
            return
        
        if not os.path.isdir(self.config['folder']):
            messagebox.showerror("Invalid Folder", "Selected folder does not exist")
            return
        
        folder = self.config['folder']
        max_age_seconds = self.config.get('max_age_hours', 1) * 3600
        
        # Find files to process
        files_to_process = []
        for file_path in Path(folder).glob("*.pdf"):
            try:
                file_age = time.time() - file_path.stat().st_mtime
                if file_age <= max_age_seconds:
                    files_to_process.append(file_path)
            except:
                pass
        
        if not files_to_process:
            messagebox.showinfo("No Files", "No PDF files found that match the criteria")
            return
        
        # Process files
        def process_files():
            for file_path in files_to_process:
                self.process_pdf(file_path)
            self.root.after(0, lambda: messagebox.showinfo("Complete", f"Processed {len(files_to_process)} file(s)"))
        
        threading.Thread(target=process_files, daemon=True).start()
        messagebox.showinfo("Processing", f"Processing {len(files_to_process)} file(s)...")

def main():
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('aqua')  # macOS native theme
    
    app = PDFMonitorWidget(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == '__main__':
    main()

