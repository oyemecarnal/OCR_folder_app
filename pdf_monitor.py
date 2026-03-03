#!/usr/bin/env python3
"""
PDF Folder Monitor - Automatically runs OCR on new PDF files
"""
import os
import json
import time
import logging
from pathlib import Path
from typing import Set, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ocrmypdf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

CONFIG_FILE = 'monitored_folders.json'
PROCESSING_FLAG = '.processing'
COMPLETED_PDFS = 'processed_pdfs.txt'


class PDFHandler(FileSystemEventHandler):
    """Handle file system events for PDF files"""
    
    def __init__(self, config_manager, stats_callback=None, pause_check=None, progress_callback=None):
        super().__init__()
        self.config_manager = config_manager
        self.processed_files: Set[str] = set()
        self.stats_callback = stats_callback  # Callback to update stats
        self.pause_check = pause_check  # Callback to check if paused
        self.progress_callback = progress_callback  # Callback to update progress
        self.current_file = None
        self.processing_queue = []  # Track files waiting to be processed
        self.load_processed_files()
        
    def load_processed_files(self):
        """Load list of already processed files to avoid reprocessing"""
        if os.path.exists(COMPLETED_PDFS):
            try:
                with open(COMPLETED_PDFS, 'r') as f:
                    self.processed_files = set(line.strip() for line in f if line.strip())
                logger.info(f"Loaded {len(self.processed_files)} previously processed files")
            except Exception as e:
                logger.error(f"Error loading processed files: {e}")
    
    def save_processed_file(self, filepath: str):
        """Mark a file as processed"""
        self.processed_files.add(filepath)
        try:
            with open(COMPLETED_PDFS, 'a') as f:
                f.write(f"{filepath}\n")
        except Exception as e:
            logger.error(f"Error saving processed file entry: {e}")
    
    def is_pdf(self, path: str) -> bool:
        """Check if file is a PDF"""
        return path.lower().endswith('.pdf')
    
    def is_processing_flag(self, path: str) -> bool:
        """Check if this is our processing flag file"""
        return os.path.basename(path) == PROCESSING_FLAG
    
    def should_process(self, filepath: str) -> bool:
        """Determine if file should be processed"""
        # Check if paused
        if self.pause_check and self.pause_check():
            return False
        
        if not self.is_pdf(filepath):
            return False
        
        # Skip if already processed
        if filepath in self.processed_files:
            return False
        
        # Skip if processing flag exists (we're currently processing this)
        flag_path = f"{filepath}.{PROCESSING_FLAG}"
        if os.path.exists(flag_path):
            return False
        
        # Only process complete files (not currently being written)
        try:
            if not os.path.exists(filepath):
                return False
            
            # Wait a bit to ensure file is fully written
            time.sleep(1)
            
            # Check if file is still being written to
            size1 = os.path.getsize(filepath)
            time.sleep(0.5)
            size2 = os.path.getsize(filepath)
            
            if size1 != size2:
                logger.info(f"File {filepath} is still being written, skipping for now")
                return False
                
        except Exception as e:
            logger.error(f"Error checking file {filepath}: {e}")
            return False
        
        return True
    
    def process_pdf(self, filepath: str, progress_callback=None):
        """Run OCR on PDF and replace original"""
        flag_path = f"{filepath}.{PROCESSING_FLAG}"
        
        try:
            # Create processing flag
            Path(flag_path).touch()
            
            logger.info(f"Processing PDF: {filepath}")
            
            # Create temporary file for OCR output
            temp_file = f"{filepath}.ocr_temp"
            
            # Track progress for this file
            self.current_file = filepath
            if progress_callback:
                progress_callback('started', filepath)
            
            # Run OCR with ocrmypdf
            # --inplace would modify directly, but we use temp file for safety
            ocrmypdf.ocr(
                filepath,
                temp_file,
                language='eng',
                progress_bar=False,
                optimize=1,  # Light optimization
                force_ocr=False,  # Skip if text layer exists
            )
            
            # Replace original with OCR'd version
            os.replace(temp_file, filepath)
            
            logger.info(f"Successfully processed: {filepath}")
            
            # Remove from queue
            if filepath in self.processing_queue:
                self.processing_queue.remove(filepath)
            
            # Mark as processed
            self.save_processed_file(filepath)
            
            # Update statistics
            if self.stats_callback:
                self.stats_callback('processed', filepath)
            
            # Clear current file
            if self.current_file == filepath:
                self.current_file = None
                if self.progress_callback:
                    self.progress_callback('completed', filepath)
            
        except ocrmypdf.exceptions.PriorOcrFoundError:
            logger.info(f"PDF {filepath} already has OCR text layer, skipping")
            # Still mark as processed since it doesn't need OCR
            self.save_processed_file(filepath)
        except Exception as e:
            logger.error(f"Error processing PDF {filepath}: {e}")
            # Update statistics
            if self.stats_callback:
                self.stats_callback('error', str(e))
            # Clean up temp file if it exists
            temp_file = f"{filepath}.ocr_temp"
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
        finally:
            # Remove processing flag
            if os.path.exists(flag_path):
                try:
                    os.remove(flag_path)
                except:
                    pass
    
    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return
        
        if self.is_processing_flag(event.src_path):
            return
        
        if self.is_pdf(event.src_path) and self.should_process(event.src_path):
            # Add to queue
            if event.src_path not in self.processing_queue:
                self.processing_queue.append(event.src_path)
                if self.progress_callback:
                    self.progress_callback('queued', event.src_path)
            # Process in background (simple approach)
            self.process_pdf(event.src_path, self.progress_callback)
    
    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return
        
        if self.is_processing_flag(event.src_path):
            return
        
        if self.is_pdf(event.src_path) and self.should_process(event.src_path):
            # Add to queue
            if event.src_path not in self.processing_queue:
                self.processing_queue.append(event.src_path)
                if self.progress_callback:
                    self.progress_callback('queued', event.src_path)
            self.process_pdf(event.src_path, self.progress_callback)


class ConfigManager:
    """Manage monitored folders configuration"""
    
    def __init__(self, config_file: str = CONFIG_FILE):
        self.config_file = config_file
        self.folders: List[str] = []
        self.load()
    
    def load(self):
        """Load monitored folders from config file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.folders = data.get('folders', [])
                    # Validate folders exist
                    self.folders = [f for f in self.folders if os.path.isdir(f)]
                logger.info(f"Loaded {len(self.folders)} monitored folders")
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                self.folders = []
        else:
            self.folders = []
            self.save()
    
    def save(self):
        """Save monitored folders to config file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({'folders': self.folders}, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def add_folder(self, folder_path: str) -> bool:
        """Add a folder to monitoring list"""
        folder_path = os.path.abspath(os.path.expanduser(folder_path))
        
        if not os.path.isdir(folder_path):
            logger.error(f"Folder does not exist: {folder_path}")
            return False
        
        if folder_path not in self.folders:
            self.folders.append(folder_path)
            self.save()
            logger.info(f"Added folder to monitoring: {folder_path}")
            return True
        else:
            logger.info(f"Folder already being monitored: {folder_path}")
            return False
    
    def remove_folder(self, folder_path: str) -> bool:
        """Remove a folder from monitoring list"""
        folder_path = os.path.abspath(os.path.expanduser(folder_path))
        
        if folder_path in self.folders:
            self.folders.remove(folder_path)
            self.save()
            logger.info(f"Removed folder from monitoring: {folder_path}")
            return True
        else:
            logger.info(f"Folder not in monitoring list: {folder_path}")
            return False
    
    def list_folders(self) -> List[str]:
        """Get list of monitored folders"""
        return self.folders.copy()


class PDFMonitor:
    """Main monitoring class"""
    
    def __init__(self, stats_callback=None, pause_check=None, progress_callback=None):
        self.config_manager = ConfigManager()
        self.observers: List[Observer] = []
        self.handler = PDFHandler(self.config_manager, stats_callback, pause_check, progress_callback)
        self.running = False
        self.stats_callback = stats_callback
        self.pause_check = pause_check
        self.progress_callback = progress_callback
    
    def start(self):
        """Start monitoring all configured folders"""
        if self.running:
            logger.warning("Monitor is already running")
            return
        
        folders = self.config_manager.list_folders()
        if not folders:
            logger.warning("No folders configured for monitoring")
            return
        
        for folder in folders:
            if os.path.isdir(folder):
                observer = Observer()
                observer.schedule(self.handler, folder, recursive=False)
                observer.start()
                self.observers.append(observer)
                logger.info(f"Started monitoring: {folder}")
            else:
                logger.warning(f"Folder does not exist, skipping: {folder}")
        
        self.running = True
        logger.info(f"PDF Monitor started monitoring {len(self.observers)} folder(s)")
    
    def stop(self):
        """Stop monitoring"""
        for observer in self.observers:
            observer.stop()
        for observer in self.observers:
            observer.join()
        self.observers.clear()
        self.running = False
        logger.info("PDF Monitor stopped")
    
    def add_folder(self, folder_path: str) -> bool:
        """Add folder and start monitoring if running"""
        if self.config_manager.add_folder(folder_path):
            if self.running:
                # Restart to include new folder
                self.stop()
                self.start()
            return True
        return False
    
    def remove_folder(self, folder_path: str) -> bool:
        """Remove folder from monitoring"""
        if self.config_manager.remove_folder(folder_path):
            if self.running:
                # Restart to exclude removed folder
                self.stop()
                self.start()
            return True
        return False


def main():
    """Main entry point"""
    import sys
    import signal
    
    monitor = PDFMonitor()
    
    # Add default folder if config is empty
    default_folder = os.path.expanduser('~/Downloads')
    if not monitor.config_manager.list_folders():
        monitor.config_manager.add_folder(default_folder)
        logger.info(f"Added default folder: {default_folder}")
    
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        logger.info("Shutting down...")
        monitor.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start monitoring
    monitor.start()
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == '__main__':
    main()

