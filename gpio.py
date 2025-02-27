#!/usr/bin/env python3
from gpiozero import Button
import time

button = Button(21)

while True:
        button.wait_for_press()
        print ("Button pressed.")
