#!/bin/bash
# SUPERVISION Pi Setup Script
# Run once on a fresh Pi after cloning the repo

echo "Installing Python 3.11..."
sudo apt install -y build-essential libssl-dev libffi-dev zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libreadline-dev libsqlite3-dev libbz2-dev
wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz
tar -xf Python-3.11.9.tgz
cd Python-3.11.9
./configure --enable-optimizations
make -j4
sudo make altinstall
cd ..

echo "Creating virtual environment..."
python3.11 -m venv venv --system-site-packages
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Done! Run 'source venv/bin/activate' then 'python main.py'"