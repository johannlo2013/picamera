import tkinter as tk
from tkinter import font as tkfont
import subprocess
import time
import os
import threading

# Paths
CAMERA_SCRIPT_PATH = "/home/mashedpotatoes/picamera/camera.py"

# Main app window
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg="white")

# Get screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Dynamic scaling based on screen size
time_font_size = int(screen_height * 0.12)
date_font_size = int(screen_height * 0.05)
label_font_size = int(screen_height * 0.03)
button_width = int(screen_width * 0.1)
button_height = int(screen_height * 0.1)
button_padding = int(screen_width * 0.02)

# Use Roboto Mono if available
available_fonts = tkfont.families()
font_family = "Roboto Mono" if "Roboto Mono" in available_fonts else "Courier"

# Time label
time_label = tk.Label(root, font=(font_family, time_font_size), fg="black", bg="white")
time_label.pack(pady=(screen_height * 0.05, 0))

# Date label
date_label = tk.Label(root, font=(font_family, date_font_size), fg="black", bg="white")
date_label.pack(pady=(screen_height * 0.01, screen_height * 0.05))

# Icons and buttons
frame = tk.Frame(root, bg="white")
frame.pack()


# Helper to run external commands and restore window
def run_and_return(command):
    def task():
        root.withdraw()
        subprocess.call(command)
        root.deiconify()
    threading.Thread(target=task).start()


def open_camera():
    run_and_return(["python3", CAMERA_SCRIPT_PATH])


def open_internet():
    run_and_return(["chromium-browser"])


def open_photos():
    run_and_return(["pcmanfm"])


def open_terminal():
    run_and_return(["lxterminal"])


buttons = [
    ("Camera", open_camera),
    ("Internet", open_internet),
    ("Pictures", open_photos),
    ("Terminal", open_terminal),
]

for name, command in buttons:
    icon_frame = tk.Frame(frame, bg="white")
    icon_frame.pack(side="left", padx=button_padding)

    button = tk.Button(
        icon_frame,
        width=button_width,
        height=button_height,
        bg="black",
        activebackground="gray",
        relief="flat",
        command=command
    )
    button.config(width=6, height=3)  # Tkinter uses text units, not pixels
    button.pack()

    label = tk.Label(icon_frame, text=name, font=(font_family, label_font_size), fg="black", bg="white")
    label.pack(pady=5)


def update_time():
    current_time = time.strftime("%H:%M")
    current_date = time.strftime("%B %d, %Y")
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    root.after(60000, update_time)


update_time()

# Escape key to exit
root.bind("<Escape>", lambda e: root.destroy())

# Small exit button
exit_button = tk.Button(
    root,
    text="X",
    font=(font_family, label_font_size),
    command=root.destroy,
    bg="red",
    fg="white",
    width=3,
    height=1
)
exit_button.place(relx=0.98, rely=0.02, anchor="ne")

root.mainloop()
