#!/bin/bash
# SUPERVISION Pi Setup Script for Python 3.11
# Run once on a fresh Pi after cloning the repo

echo "Installing system dependencies..."
sudo apt install -y python3-picamera2 libcap-dev


# CUPS configuration
sudo apt install -y cups python3-venv git
sudo cupsctl --remote-admin
sudo systemctl restart cups
sudo usermod -aG lpadmin arcadia


echo "Creating virtual environment..."
python3 -m venv venv --system-site-packages
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements_pi.txt

# Download CP1500 PPD driver
wget -q https://gist.githubusercontent.com/benjaminkott/e293147dd0ea9e6fa7f1194567a5d1ba/raw/00975a9a713e24417a476f923d8e2b4c2a6529b4/Canon_SELPHY_CP1500.ppd

# Add Selphy printer with correct driver
sudo lpadmin -p Selphy -E -v usb://Canon/SELPHY%20CP1500?serial=CV25071808075718 -m gutenprint.5.3://canon-cp1300/expert
sudo lpadmin -d Selphy
sudo lpadmin -p Selphy -o StpiShrinkOutput=Shrink
sudo lpadmin -p Selphy -o PageSize=Postcard

echo "Downloading MediaPipe models..."
cd computervision/mediapipe/detection/ 
wget -q https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
wget -q https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task
wget -q https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task
wget https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task

#system package for Thermal Printer
sudo apt install libusb-1.0-0 -y
sudo usermod -aG lp arcadia
echo "usblp" | sudo tee -a /etc/modules
sudo modprobe usblp  # loads it immediately without needing reboot



echo "Done! Run 'source venv/bin/activate' then 'python3 main.py'"