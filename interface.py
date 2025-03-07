import tkinter as tk
from tkinter import font as tkfont
import subprocess
import time
import os

# Paths
CAMERA_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "camera_script.py")

# Main app window
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg="white")

# Use Roboto Mono if available
available_fonts = tkfont.families()
font_family = "Roboto Mono" if "Roboto Mono" in available_fonts else "Courier"

# Smaller font sizes
time_font_size = 50
date_font_size = 20
label_font_size = 10
button_size = 60  # pixels

# Time label
time_label = tk.Label(root, font=(font_family, time_font_size), fg="black", bg="white")
time_label.pack(pady=(40, 0))

# Date label
date_label = tk.Label(root, font=(font_family, date_font_size), fg="black", bg="white")
date_label.pack(pady=(5, 30))

# Icons and buttons
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

buttons = [
    ("Camera", open_camera),
    ("Internet", open_internet),
    ("Pictures", open_photos),
    ("Terminal", open_terminal),
]

for name, command in buttons:
    icon_frame = tk.Frame(frame, bg="white")
    icon_frame.pack(side="left", padx=10)

    button = tk.Button(
        icon_frame,
        width=button_size,
        height=button_size,
        bg="black",
        activebackground="gray",
        relief="flat",
        command=command
    )
    button.config(width=5, height=2)  # Smaller button size
    button.pack()

    label = tk.Label(icon_frame, text=name, font=(font_family, label_font_size), fg="black", bg="white")
    label.pack(pady=3)

def update_time():
    current_time = time.strftime("%H:%M")
    current_date = time.strftime("%B %d, %Y")
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    root.after(60000, update_time)

update_time()

# Escape key to exit
root.bind("<Escape>", lambda e: root.destroy())

# Optional small exit button at the top-right corner
exit_button = tk.Button(
    root,
    text="X",
    font=(font_family, 10),
    command=root.destroy,
    bg="red",
    fg="white",
    width=3,
    height=1
)
exit_button.place(relx=0.98, rely=0.02, anchor="ne")

root.mainloop()
