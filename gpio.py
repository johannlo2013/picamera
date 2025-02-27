#!/usr/bin/env python3
from gpiozero import Button
import time

button = Button(16)

while True:
        button.wait_for_press()
        print("Button pressed.")
        time.sleep(2)
