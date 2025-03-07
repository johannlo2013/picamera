import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import subprocess
import time
import os
import threading

# Paths
CAMERA_SCRIPT_PATH = "/home/mashedpotatoes/picamera/camera.py"

root = tk.Tk()
root.attributes('-fullscreen', True)

# 🎨 Colors
bg_color = "#222222"
text_color = "#FFFFFF"
exit_button_color = "#FF5555"
exit_button_text = "#FFFFFF"

root.configure(bg=bg_color)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

time_font_size = int(screen_height * 0.10)
date_font_size = int(screen_height * 0.045)
label_font_size = int(screen_height * 0.035)
button_padding = int(screen_width * 0.03)
icon_size = int(screen_height * 0.12)

available_fonts = tkfont.families()
font_family = "Roboto Mono" if "Roboto Mono" in available_fonts else "Courier"

time_label = tk.Label(root, font=(font_family, time_font_size), fg=text_color, bg=bg_color)
time_label.pack(pady=(screen_height * 0.05, 0))

date_label = tk.Label(root, font=(font_family, date_font_size), fg=text_color, bg=bg_color)
date_label.pack(pady=(screen_height * 0.01, screen_height * 0.06))

frame = tk.Frame(root, bg=bg_color)
frame.pack()


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
    ("Camera", open_camera, "camera.png"),
    ("Internet", open_internet, "internet.png"),
    ("Pictures", open_photos, "pictures.png"),
    ("Terminal", open_terminal, "terminal.png"),
]

# Load and store images to prevent garbage collection
images = {}

for name, command, icon_file in buttons:
    icon_frame = tk.Frame(frame, bg=bg_color)
    icon_frame.pack(side="left", padx=button_padding, pady=10)

    img = Image.open(icon_file)
    img = img.resize((icon_size, icon_size), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    images[icon_file] = photo  # Save reference

    button = tk.Button(
        icon_frame,
        image=photo,
        bg=bg_color,
        activebackground=bg_color,
        relief="flat",
        bd=0,
        highlightthickness=0,
        command=command
    )
    button.pack()

    label = tk.Label(icon_frame, text=name, font=(font_family, label_font_size), fg=text_color, bg=bg_color)
    label.pack(pady=5)


def update_time():
    current_time = time.strftime("%H:%M")
    current_date = time.strftime("%B %d, %Y")
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    root.after(60000, update_time)


update_time()

root.bind("<Escape>", lambda e: root.destroy())

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
