# rpicam v0 interface
# designed to run on raspberry pi to control camera
# johann lo (johannlo@thesunbeaming.co)

import tkinter as tk
from tkinter import ttk, messagebox
from picamera2 import Picamera2
from PIL import Image, ImageTk
import time
import datetime
import os
import RPi.GPIO as GPIO
import subprocess
import json
from threading import Thread
import logging
from pathlib import Path

class CameraConfig:
    def __init__(self):
        self.BUTTON_PIN = 16
        self.MEDIA_DIR = Path("media")
        self.CONFIG_FILE = Path("camera_config.json")
        self.DEFAULT_RESOLUTION = (1920, 1080)
        self.PREVIEW_RESOLUTION = (480, 270)
        self.FPS = 30
        self.THEME = {
            'bg': '#1a1a1a',
            'fg': '#ffffff',
            'button_bg': '#2d2d2d',
            'button_fg': '#ffffff',
            'accent': '#007bff',
            'warning': '#dc3545'
        }
        self.setup_logging()
        self.load_config()
        self.setup_gpio()
        self.ensure_directories()

    def setup_logging(self):
        logging.basicConfig(
            filename='camera_app.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def load_config(self):
        try:
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    for key, value in config.items():
                        if hasattr(self, key):
                            setattr(self, key, value)
        except Exception as e:
            logging.error(f"failed to load config: {e}")

    def save_config(self):
        try:
            config_dict = {
                key: value for key, value in self.__dict__.items()
                if not key.startswith('_') and isinstance(value, (str, int, float, list, dict))
            }
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config_dict, f)
        except Exception as e:
            logging.error(f"failed to save config: {e}")

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def ensure_directories(self):
        self.MEDIA_DIR.mkdir(parents=True, exist_ok=True)

class CustomButton(tk.Button):
    def __init__(self, master, theme, **kwargs):
        super().__init__(master, **kwargs)
        self.theme = theme
        self.configure(
            relief=tk.FLAT,
            borderwidth=0,
            padx=15,
            pady=8,
            font=("Inter", 12),
            cursor="hand2"
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self['background'] = self.theme['accent']

    def on_leave(self, e):
        self['background'] = self.theme['button_bg']

class CameraSelector:
    def __init__(self, config):
        self.config = config
        self.window = tk.Tk()
        self.window.title("Camera Selection")
        self.window.configure(bg=config.THEME['bg'])
        self.selected_camera = tk.IntVar(value=0)
        self.setup_ui()

    def setup_ui(self):
        cameras = Picamera2.global_camera_info()
        if not cameras:
            messagebox.showerror("Error", "No cameras detected!")
            self.window.destroy()
            return

        tk.Label(
            self.window,
            text="Select Camera",
            font=("Inter", 16, "bold"),
            bg=self.config.THEME['bg'],
            fg=self.config.THEME['fg']
        ).pack(pady=20)

        for i, cam in enumerate(cameras):
            tk.Radiobutton(
                self.window,
                text=cam.get('ModelName', f'Camera {i}'),
                variable=self.selected_camera,
                value=i,
                bg=self.config.THEME['bg'],
                fg=self.config.THEME['fg'],
                selectcolor=self.config.THEME['button_bg']
            ).pack(pady=5, padx=20, anchor='w')

        CustomButton(
            self.window,
            theme=self.config.THEME,
            text="Confirm",
            command=self.window.destroy,
            bg=self.config.THEME['button_bg'],
            fg=self.config.THEME['fg']
        ).pack(pady=20)

    def get_selection(self):
        self.window.mainloop()
        return self.selected_camera.get()

class CameraApp:
    def __init__(self, root, camera_index, config):
        self.root = root
        self.config = config
        self.camera_index = camera_index
        self.video_recording = False
        self.clock_clicks = 0  
        self.last_click_time = 0  
        self.setup_ui()
        self.initialize_camera()
        self.start_update_threads()

    def setup_ui(self):
        self.root.title("rpicam v0")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=self.config.THEME['bg'])

        self.main_container = tk.Frame(
            self.root,
            bg=self.config.THEME['bg']
        )
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.preview_label = tk.Label(
            self.main_container,
            bg=self.config.THEME['bg']
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True)

        self.setup_control_panel()

    def setup_control_panel(self):
        control_panel = tk.Frame(
            self.main_container,
            bg=self.config.THEME['bg']
        )
        control_panel.pack(fill=tk.X, pady=10)

        self.status_frame = tk.Frame(
            control_panel,
            bg=self.config.THEME['bg']
        )
        self.status_frame.pack(side=tk.LEFT, padx=10)

        self.clock_label = tk.Label(
            self.status_frame,
            font=("Inter", 14),
            bg=self.config.THEME['bg'],
            fg=self.config.THEME['fg']
        )
        self.clock_label.pack(side=tk.LEFT)
        self.clock_label.bind('<Button-1>', self.on_clock_click)

        self.recording_indicator = tk.Label(
            self.status_frame,
            text="●",
            font=("Inter", 14),
            bg=self.config.THEME['bg'],
            fg=self.config.THEME['bg']
        )
        self.recording_indicator.pack(side=tk.LEFT, padx=5)

        buttons_frame = tk.Frame(
            control_panel,
            bg=self.config.THEME['bg']
        )
        buttons_frame.pack(side=tk.RIGHT)

        self.capture_btn = CustomButton(
            buttons_frame,
            theme=self.config.THEME,
            text="Take Photo",
            command=self.capture_photo,
            bg=self.config.THEME['button_bg'],
            fg=self.config.THEME['fg']
        )
        self.capture_btn.pack(side=tk.LEFT, padx=5)

        self.record_btn = CustomButton(
            buttons_frame,
            theme=self.config.THEME,
            text="Start Recording",
            command=self.toggle_recording,
            bg=self.config.THEME['button_bg'],
            fg=self.config.THEME['fg']
        )
        self.record_btn.pack(side=tk.LEFT, padx=5)

        self.exit_btn = CustomButton(
            buttons_frame,
            theme=self.config.THEME,
            text="Exit",
            command=self.shutdown,
            bg=self.config.THEME['warning'],
            fg=self.config.THEME['fg']
        )
        self.exit_btn.pack(side=tk.LEFT, padx=5)

    def initialize_camera(self):
        try:
            self.camera = Picamera2(self.camera_index)
            preview_config = self.camera.create_preview_configuration(
                main={"size": self.config.PREVIEW_RESOLUTION, "format": "RGB888"},
                raw={"size": self.config.DEFAULT_RESOLUTION}
            )
            self.camera.configure(preview_config)
            self.camera.start()
            logging.info(f"camera {self.camera_index} initialized successfully")
        except Exception as e:
            logging.error(f"camera initialization failed: {e}")
            messagebox.showerror("Error", "Failed to initialize camera")
            self.root.destroy()

    def start_update_threads(self):
        Thread(target=self.update_preview, daemon=True).start()
        Thread(target=self.update_clock, daemon=True).start()

    def update_preview(self):
        while True:
            try:
                if not self.video_recording:
                    frame = self.camera.capture_array()
                    image = Image.fromarray(frame)
                    image = image.resize(self.config.PREVIEW_RESOLUTION)
                    photo = ImageTk.PhotoImage(image=image)
                    self.preview_label.configure(image=photo)
                    self.preview_label.image = photo
                time.sleep(1/self.config.FPS)
            except Exception as e:
                logging.error(f"preview update failed: {e}")
                time.sleep(1)

    def update_clock(self):
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.clock_label.configure(text=current_time)
            time.sleep(1)

    def on_clock_click(self, event):
        current_time = time.time()

        if current_time - self.last_click_time > 2:
            self.clock_clicks = 0
        
        self.last_click_time = current_time
        self.clock_clicks += 1
        
        if self.clock_clicks >= 5:
            self.clock_clicks = 0 
            self.launch_browser()
    
    def launch_browser(self):
        try:
            subprocess.Popen(['lxpanelctl', 'menu'])
            logging.info("lxpanelctl menu launched")
        except Exception as e:
            logging.error(f"failed to launch menu: {e}")
            self.show_notification("Failed to launch menu", error=True)

    def capture_photo(self):
        try:
            filename = self.config.MEDIA_DIR / f"photo_{int(time.time())}.jpg"
            self.camera.capture_file(str(filename))
            logging.info(f"photo captured: {filename}")
            self.show_notification("Photo captured successfully")
        except Exception as e:
            logging.error(f"photo capture failed: {e}")
            self.show_notification("Failed to capture photo", error=True)

    def toggle_recording(self):
        if self.video_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        try:
            self.video_filename = self.config.MEDIA_DIR / f"video_{int(time.time())}.mp4"
            self.camera.start_and_record_video(str(self.video_filename))
            self.video_recording = True
            self.record_btn.configure(text="Stop Recording")
            self.recording_indicator.configure(fg=self.config.THEME['warning'])
            logging.info(f"started recording: {self.video_filename}")
        except Exception as e:
            logging.error(f"failed to start recording: {e}")
            self.show_notification("Failed to start recording", error=True)

    def stop_recording(self):
        try:
            self.camera.stop()

            self.camera.stop_recording()
            self.video_recording = False
            self.record_btn.configure(text="Start Recording")
            self.recording_indicator.configure(fg=self.config.THEME['bg'])
            logging.info(f"stopped recording: {self.video_filename}")

            preview_config = self.camera.create_preview_configuration(
                main={"size": self.config.PREVIEW_RESOLUTION, "format": "RGB888"},
                raw={"size": self.config.DEFAULT_RESOLUTION}
            )
            self.camera.configure(preview_config)
            self.camera.start()
            
            self.show_notification("Recording saved successfully")
        except Exception as e:
            logging.error(f"failed to stop recording: {e}")
            self.show_notification("Failed to stop recording", error=True)
            try:
                self.initialize_camera()
            except Exception as recovery_error:
                logging.error(f"failed to recover camera: {recovery_error}")

    def switch_camera(self):
        self.camera.stop()
        selector = CameraSelector(self.config)
        new_index = selector.get_selection()
        if new_index != self.camera_index:
            self.camera_index = new_index
            self.initialize_camera()

    def show_notification(self, message, error=False):
        color = self.config.THEME['warning'] if error else self.config.THEME['accent']
        notification = tk.Label(
            self.root,
            text=message,
            font=("Inter", 12),
            bg=color,
            fg=self.config.THEME['fg'],
            padx=20,
            pady=10
        )
        notification.place(relx=0.5, rely=0.1, anchor='n')
        self.root.after(2000, notification.destroy)

    def shutdown(self):
        if messagebox.askyesno("Confirm Shutdown", "Are you sure you want to exit?"):
            self.camera.stop()
            GPIO.cleanup()
            self.root.destroy()
            os.system("sudo shutdown -h now")

def main():
    try:
        config = CameraConfig()
        selector = CameraSelector(config)
        camera_index = selector.get_selection()
        
        root = tk.Tk()
        app = CameraApp(root, camera_index, config)
        root.mainloop()
    except Exception as e:
        logging.critical(f"application crashed: {e}")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()