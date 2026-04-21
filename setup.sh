#!/bin/bash
# SUPERVISION Pi Setup Script for Python 3.11
# Run once on a fresh Pi after cloning the repo

echo "Installing system dependencies..."
sudo apt install -y python3-picamera2 libcap-dev

echo "Creating virtual environment..."
python3 -m venv venv --system-site-packages
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Done! Run 'source venv/bin/activate' then 'python main.py'"