#!/usr/bin/env python3
"""
CLI tool to manage monitored folders
"""
import sys
import argparse
from pdf_monitor import ConfigManager

def main():
    parser = argparse.ArgumentParser(
        description='Manage folders monitored for PDF OCR',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_folders.py add /path/to/folder
  python manage_folders.py add ~/Documents/Inbox
  python manage_folders.py remove /path/to/folder
  python manage_folders.py list
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Add folder command
    add_parser = subparsers.add_parser('add', help='Add a folder to monitoring list')
    add_parser.add_argument('folder', help='Path to folder to monitor')
    
    # Remove folder command
    remove_parser = subparsers.add_parser('remove', help='Remove a folder from monitoring list')
    remove_parser.add_argument('folder', help='Path to folder to remove')
    
    # List folders command
    list_parser = subparsers.add_parser('list', help='List all monitored folders')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    config = ConfigManager()
    
    if args.command == 'add':
        if config.add_folder(args.folder):
            print(f"✓ Added folder: {args.folder}")
            sys.exit(0)
        else:
            print(f"✗ Failed to add folder: {args.folder}")
            sys.exit(1)
    
    elif args.command == 'remove':
        if config.remove_folder(args.folder):
            print(f"✓ Removed folder: {args.folder}")
            sys.exit(0)
        else:
            print(f"✗ Folder not found in list: {args.folder}")
            sys.exit(1)
    
    elif args.command == 'list':
        folders = config.list_folders()
        if folders:
            print("Monitored folders:")
            for i, folder in enumerate(folders, 1):
                print(f"  {i}. {folder}")
        else:
            print("No folders currently being monitored")
        sys.exit(0)


if __name__ == '__main__':
    main()



