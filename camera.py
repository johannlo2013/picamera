#!/usr/bin/env python3
import cv2
import tkinter as tk
import time
import platform
import threading
from PIL import Image, ImageTk
import os

# Determine the appropriate camera index
camera_index = 0  # Default for built-in webcams
if platform.system() == "Darwin":  # macOS
    camera_index = 0
elif platform.system() == "Windows":  # Windows
    camera_index = 0

# Initialize the camera
cap = cv2.VideoCapture(camera_index)
cap.set(3, 480)  # Set width
cap.set(4, 360)  # Set height
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

frame = int(time.time())

# Load custom font
font_path = os.path.join(os.path.dirname(__file__), "RobotoMono-Regular.ttf")
custom_font = (font_path, 16)

def update_preview():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((480, 360))
        imgtk = ImageTk.PhotoImage(image=img)
        preview_label.imgtk = imgtk
        preview_label.config(image=imgtk)
    root.after(10, update_preview)

def capture_image():
    global frame
    ret, image = cap.read()
    if ret:
        filename = f'capture_{frame}.jpg'
        cv2.imwrite(filename, image)
        status_label.config(text=f'Image saved as: {filename}', fg="green")
        frame += 1
    else:
        status_label.config(text="Error: Failed to capture image", fg="red")

# Create the GUI interface
root = tk.Tk()
root.title("Camera Capture Interface")
root.attributes('-fullscreen', True)
root.configure(bg="white")

# Add preview label
preview_label = tk.Label(root, bg="white")
preview_label.pack(pady=10)

# Button frame to keep buttons close together
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

# Function to create rounded buttons
def create_rounded_button(parent, text, command, bg, fg):
    button = tk.Button(parent, text=text, command=command, font=custom_font, bg=bg, fg=fg, padx=20, pady=10, bd=0, relief="flat")
    button.config(highlightbackground=bg, highlightthickness=0)
    button.pack(side=tk.LEFT, padx=10)  # Arrange buttons next to each other
    return button

# Add capture button
capture_button = create_rounded_button(button_frame, "Capture Image", capture_image, "blue", "black")

# Add exit button
exit_button = create_rounded_button(button_frame, "Exit", root.destroy, "red", "black")

# Add status label
status_label = tk.Label(root, text="", font=custom_font, bg="white")
status_label.pack(pady=10)

# Start live preview in the GUI
update_preview()

# Start the GUI event loop
root.mainloop()

# Release the camera when the window is closed
cap.release()
cv2.destroyAllWindows()
