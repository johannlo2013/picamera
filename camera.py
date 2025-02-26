#!/usr/bin/env python3
import tkinter as tk
from picamera2 import Picamera2, Preview
import time
import threading

# Function to capture images
def capture_image():
    global frame
    filename = '/home/pi/Pictures/%03d.jpg' % frame
    picam2.switch_mode_and_capture_file(capture_config, filename)
    print(f'Image captured: {filename}')
    frame += 1

# Function to start preview in Tkinter window
def start_preview():
    global picam2
    picam2.start_preview(Preview.QT)
    picam2.configure(preview_config)
    picam2.start()
    print("Preview started")
    time.sleep(1)

# Initialize the Picamera2 object
picam2 = Picamera2()
frame = int(time.time())

# Set up preview configuration and capture configuration
preview_config = picam2.create_preview_configuration()
capture_config = picam2.create_still_configuration()

# Create the GUI interface
root = tk.Tk()
root.title("picamera.sh")
root.attributes('-fullscreen', True)  # Make the window fullscreen
root.configure(bg='black')  # Background color black to match the preview

# Create a Canvas widget for preview
canvas = tk.Canvas(root, bg='black', width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack(fill=tk.BOTH, expand=True)

# Add a capture button to the interface
capture_button = tk.Button(root, text="Capture", command=capture_image, font=('Arial', 24), bd=20)
capture_button.pack(pady=20)

# Start the preview and GUI in separate thread to avoid blocking
def preview_thread():
    start_preview()

# Use a separate thread to handle the camera preview without freezing the GUI
thread = threading.Thread(target=preview_thread)
thread.daemon = True
thread.start()

# Start the Tkinter event loop
root.mainloop()

