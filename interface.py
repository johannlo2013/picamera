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

# 🎨 Theme Colors
bg_color = "#222222"  # Dark mode background
text_color = "#FFFFFF"  # White text
button_color = "#444444"  # Dark gray buttons
button_active = "#666666"  # Lighter gray when pressed
exit_button_color = "#FF5555"  # Red exit button
exit_button_text = "#FFFFFF"

root.configure(bg=bg_color)

# Get screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Dynamic scaling based on screen size
time_font_size = int(screen_height * 0.10)
date_font_size = int(screen_height * 0.045)
label_font_size = int(screen_height * 0.035)
button_size = int(screen_height * 0.12)  # Button height/width
button_padding = int(screen_width * 0.03)  # More padding

# Use Roboto Mono if available
available_fonts = tkfont.families()
font_family = "Roboto Mono" if "Roboto Mono" in available_fonts else "Courier"

# Time label
time_label = tk.Label(root, font=(font_family, time_font_size), fg=text_color, bg=bg_color)
time_label.pack(pady=(screen_height * 0.05, 0))

# Date label
date_label = tk.Label(root, font=(font_family, date_font_size), fg=text_color, bg=bg_color)
date_label.pack(pady=(screen_height * 0.01, screen_height * 0.06))

# Icons and buttons container
frame = tk.Frame(root, bg=bg_color)
frame.pack()


# Helper function to run external commands and restore the UI
def run_and_return(command):
    def task():
        root.withdraw()
        subprocess.call(command)
        root.deiconify()
    threading.Thread(target=task).start()


# Button actions
def open_camera():
    run_and_return(["python3", CAMERA_SCRIPT_PATH])


def open_internet():
    run_and_return(["chromium-browser"])


def open_photos():
    run_and_return(["pcmanfm"])


def open_terminal():
    run_and_return(["lxterminal"])


# Button definitions
buttons = [
    ("Camera", open_camera),
    ("Internet", open_internet),
    ("Pictures", open_photos),
    ("Terminal", open_terminal),
]

# Create buttons with more padding and rounded edges
for name, command in buttons:
    icon_frame = tk.Frame(frame, bg=bg_color)
    icon_frame.pack(side="left", padx=button_padding, pady=10)  # Added vertical padding

    button = tk.Button(
        icon_frame,
        text=" ",  # Invisible text (pure shape button)
        width=button_size,
        height=button_size,
        bg=button_color,
        activebackground=button_active,
        relief="flat",
        bd=0,
        highlightthickness=0,
        command=command
    )
    button.config(width=8, height=4)  # Adjust text-based sizing
    button.pack()

    label = tk.Label(icon_frame, text=name, font=(font_family, label_font_size), fg=text_color, bg=bg_color)
    label.pack(pady=5)


# Update time every minute
def update_time():
    current_time = time.strftime("%H:%M")
    current_date = time.strftime("%B %d, %Y")
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    root.after(60000, update_time)


update_time()

# Escape key to exit
root.bind("<Escape>", lambda e: root.destroy())

# 🛑 Improved Exit Button (fixed white background issue)
exit_button = tk.Button(
    root,
    text="X",
    font=(font_family, label_font_size),
    command=root.destroy,
    bg=exit_button_color,
    fg=exit_button_text,
    width=3,
    height=1,
    relief="flat",
    bd=0,
    highlightthickness=0,
    activebackground="#FF7777"
)
exit_button.place(relx=0.98, rely=0.02, anchor="ne")

root.mainloop()
