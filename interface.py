import tkinter as tk
from tkinter import font as tkfont
import subprocess
import time
import os

# Paths
CAMERA_SCRIPT_PATH = os.path.join("/home/mashedpotatoes/picamera/camera.py")

# Main app window
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg="white")

# Use Roboto Mono if available
available_fonts = tkfont.families()
font_family = "Roboto Mono" if "Roboto Mono" in available_fonts else "Courier"

# Time label
time_label = tk.Label(root, font=(font_family, 80), fg="black", bg="white")
time_label.pack(pady=(100, 0))

# Date label
date_label = tk.Label(root, font=(font_family, 30), fg="black", bg="white")
date_label.pack(pady=(10, 50))

# Icons (black squares with labels)
frame = tk.Frame(root, bg="white")
frame.pack()


def open_camera():
    subprocess.Popen(["python3", CAMERA_SCRIPT_PATH])


def open_internet():
    subprocess.Popen(["chromium-browser"])


def open_photos():
    subprocess.Popen(["pcmanfm"])


def open_terminal():
    subprocess.Popen(["lxterminal"])


# Button details
buttons = [
    ("Camera", open_camera),
    ("Internet", open_internet),
    ("Pictures", open_photos),
    ("Terminal", open_terminal),
]

exit_button = tk.Button(
    root,
    text="Exit",
    font=(font_family, 12),
    command=root.destroy,
    bg="red",
    fg="white"
)
exit_button.place(relx=0.95, rely=0.05, anchor="ne")

for name, command in buttons:
    icon_frame = tk.Frame(frame, bg="white")
    icon_frame.pack(side="left", padx=20)

    button = tk.Button(
        icon_frame,
        width=8,
        height=4,
        bg="black",
        activebackground="gray",
        relief="flat",
        command=command
    )
    button.pack()

    label = tk.Label(icon_frame, text=name, font=(font_family, 12), fg="black", bg="white")
    label.pack(pady=5)


def update_time():
    current_time = time.strftime("%H:%M")
    current_date = time.strftime("%B %d, %Y")
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    root.after(60000, update_time)  # Update every minute


update_time()

# Exit fullscreen with Escape key
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
