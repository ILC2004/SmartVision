# SmartVision

Real-Time Visual Monitoring with Python & OpenCV 

Description
Smart Vision Toolkit is a simple, cross-platform desktop application that lets you take webcam photos, record short video clips, and run a live motion-detection feed with bounding-box highlights. All captures are timestamped and saved into a local “recordings” folder.

Features
• Graphical user interface built with Tkinter
• Photo capture: press SPACE in the preview to snap a JPEG
• Video recording: 10-second clips or ESC to stop early
• Live motion detection: green boxes highlight moving objects, with an optional beep
• Auto-organized output: all media stored under recordings with timestamps

Getting Started

Prerequisites
• Python 3.6 or higher
• OpenCV for Python (pip install opencv-python)
• A working webcam
• On Windows, winsound is used for the beep; on other OSes you can remove or replace that call

Clone and Run

    Clone the repository:
    git clone https://github.com/ILC2004/smart-vision-toolkit.git

    Change into the project folder:
    cd smart-vision-toolkit

    Run the app:
    python smart_vision.py

On first run the script will create a “recordings” folder next to itself. Your captured photos and videos will appear there.

############################################################################################################################

Smart Vision Toolkit on Raspberry Pi

    Prerequisites

        A Raspberry Pi running Raspberry Pi OS (Bullseye or later)

        Python 3.7 or higher (comes with recent Pi OS)

        A USB webcam or the official Pi Camera module

        Internet connection to install packages

    Enable the Pi Camera (only if using the Pi Camera module)

        Open a terminal (or SSH in) and run:
        sudo raspi-config

        Choose “Interface Options” then “Camera” and select “Enable”

        Reboot when prompted

    Update the system and install dependencies

        In a terminal run:
        sudo apt update && sudo apt upgrade -y
        sudo apt install -y python3-opencv python3-tk

        (Optional for sound alerts)
        sudo apt install -y beep

    Clone the repository

        In your home folder run:
        git clone https://github.com/yourusername/smart-vision-toolkit.git
        cd smart-vision-toolkit

    Install any extra Python packages

        If you need the latest OpenCV or other extras:
        pip3 install opencv-python

        If you’ll convert videos/GIFs later, you may also install ffmpeg:
        sudo apt install -y ffmpeg

    Adjust the beep alert (optional)

        The Windows version uses winsound.Beep(). On Pi you can either:
        • Comment out or remove the winsound.Beep line
        • Or replace it with a system call, for example:
        import os
        os.system("beep -f 1000 -l 200")

    Run the application

        From inside the project folder run:
        python3 smart_vision.py

        A window will open with three buttons:
        • 📸 Take Photo (press SPACE to capture, ESC to cancel)
        • 🎥 Record Video (records 10 seconds, or press ESC to stop early)
        • 🟢 Live CCTV (shows real-time motion boxes; press ESC in the video window to stop)

    Where output goes

        A folder named “recordings” is created next to smart_vision.py

        Photos and videos will be saved there with timestamped filenames
