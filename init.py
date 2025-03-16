import tkinter as tk
from picamera2 import Picamera2
from PIL import Image, ImageTk
import time
import threading
import datetime
import os
import RPi.GPIO as GPIO
import subprocess

BUTTON_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

def select_camera():
    camwindow = tk.Tk()
    camwindow.title("Select Camera")
    camwindow.geometry("480x360")
    camwindow.configure(bg='black')
    
    cameras = Picamera2.global_camera_info()
    if not cameras:
        print("No cameras detected.")
        camwindow.destroy()
        exit()
    
    selected_camera = tk.IntVar()
    
    tk.Label(camwindow, text="Select a Camera", font=("Inter", 16), fg="white", bg="black").pack(pady=10)
    
    for i, cam in enumerate(cameras):
        cam_name = cam.get('ModelName', f'Unknown Camera {i}')
        tk.Radiobutton(camwindow, text=cam_name, variable=selected_camera, value=i, font=("Inter", 14), fg="white", bg="black", selectcolor='gray').pack(anchor='w', padx=20)
    
    def confirm():
        camwindow.destroy()
    
    def close():
        camwindow.destroy()
        exit()
    
    tk.Button(camwindow, text="Confirm", font=("Inter", 16), command=confirm).pack(pady=20)
    camwindow.mainloop()
    
    return selected_camera.get()

class CameraApp:
    def __init__(self, root, camera_index):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.geometry("480x360")
        self.root.configure(bg='black')
        
        self.picam2 = Picamera2(camera_index)
        self.picam2.preview_configuration.main.size = (480, 270)
        self.picam2.preview_configuration.main.format = "RGB888"
        self.picam2.configure("preview")
        self.picam2.start()
        
        self.video_recording = False
        self.last_press_time = 0
        self.video_filename = ""
        self.clock_tap_count = 0
        
        self.canvas = tk.Label(root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.button_frame = tk.Frame(root, bg='black')
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.clock_label = tk.Label(self.button_frame, text="", font=("Inter", 16), fg="white", bg="black")
        self.clock_label.pack(side=tk.LEFT, padx=10)
        self.clock_label.bind("<Button-1>", self.clocktap)
        
        self.video_button = tk.Button(self.button_frame, text="Record", font=("Inter", 14), command=self.togglevid)
        self.video_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        self.close_button = tk.Button(self.button_frame, text="Exit", font=("Inter", 14), fg="white", bg="red", command=root.quit)
        self.close_button.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        self.update()
        self.updclock()
        self.setupgpio()
    
    def update(self):
        frame = self.picam2.capture_array()
        image = Image.fromarray(frame)
        image = image.resize((480, 270))
        self.photo = ImageTk.PhotoImage(image=image)
        self.canvas.config(image=self.photo)
        self.root.after(100, self.update_preview)
    
    def updclock(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)
    
    def capture(self):
        filename = os.path.join(MEDIA_DIR, f"photo_{int(time.time())}.jpg")
        self.picam2.capture_file(filename)
        print(f"Photo saved: {filename}")
    
    def togglevid(self):
        if self.video_recording:
            self.stoprec()
        else:
            self.startrec()
    
    def startrec(self):
        self.video_filename = os.path.join(MEDIA_DIR, f"video_{int(time.time())}.mp4")
        self.picam2.start_and_record_video(self.video_filename)
        self.video_recording = True
        print(f"Recording video: {self.video_filename}")
    
    def stoprec(self):
        self.picam2.stop_recording()
        self.video_recording = False
        print(f"Video saved: {self.video_filename}")
        self.picam2.start()
    
    def callback(self, channel):
        self.capture()

    def setupgpio(self):
        GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=self.callback, bouncetime=300)
    
    def clocktap(self, event):
        self.clock_tap_count += 1
        if self.clock_tap_count >= 5:
            self.clock_tap_count = 0
            subprocess.run(["chromium-browser", "--start-maximized"], check=False)

if __name__ == "__main__":
    try:
        selected_index = select_camera()
        root = tk.Tk()
        app = CameraApp(root, selected_index)
        root.mainloop()
    finally:
        GPIO.cleanup()
