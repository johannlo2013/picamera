#!/usr/bin/env python3
import tkinter as tk
from picamera2 import Picamera2, Preview
import time

# Create a function to capture images
def capture_image():
    global frame
    filename = '/home/pi/Pictures/%03d.jpg' % frame
    picam2.switch_mode_and_capture_file(capture_config, filename)
    print(f'Image captured: {filename}')
    frame += 1

# Initialize the Picamera2 object
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

    # Turn on full-time autofocus.
    picam2.set_controls({"AfMode": 2, "AfTrigger": 0})

    # Create the GUI interface
    root = tk.Tk()
    root.title("Camera Capture Interface")
    root.geometry("300x150")

    # Add a capture button to the interface
    capture_button = tk.Button(root, text="Capture Image", command=capture_image)
    capture_button.pack(pady=20)

    # Start the GUI event loop
    root.mainloop()
