#!/usr/bin/env python3
import os
from gpiozero import Button
from picamera2 import Picamera2, Preview
import time

# Directory where images will be saved
picture_dir = '/home/mashedpotatoes/picamera/pictures'

# Check if the directory exists, create it if it doesn't
if not os.path.exists(picture_dir):
    os.makedirs(picture_dir)
    print(f"Directory {picture_dir} created.")

button = Button(21)

with Picamera2() as picam2:
    frame = int(time.time())

    # Set up QT preview window.
    picam2.start_preview(Preview.QT)
    preview_config = picam2.create_preview_configuration()
    capture_config = picam2.create_still_configuration()
    picam2.configure(preview_config)
    picam2.start()
    time.sleep(1)
    print("Preview started")

    # Wait for button press. When pressed, take picture.
    while True:
        button.wait_for_press()
        filename = os.path.join(picture_dir, f'{frame:03d}.jpg')  # Ensure proper path and filename
        picam2.switch_mode_and_capture_file(capture_config, filename)
        print(f'Image captured: {filename}')
        frame += 1
