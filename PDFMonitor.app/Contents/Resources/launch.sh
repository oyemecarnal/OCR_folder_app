#!/bin/bash
cd "$(dirname "$(dirname "$(dirname "$(dirname "$0")")")")"
exec python3 pdf_monitor_app.py

