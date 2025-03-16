# picamera interface 0
## materials
- waveshare 3.5 inch touchscreen
- raspberry pi 4b or later
- camera module(s)
- usb-c power bank or li-ion battery
- usb-c to usb-c cable
- micro-usb to hdmi cable
- hdmi cable
- wired keyboard and mouse
- 32gb microsd card
- wired buttons
- self-designed case (optional)
## instructions
### assembly
1. unbox all the materials.
2. connect the wired button to the gpio pins. one should be on a gnd and one should be on the bcm 21 pin. (refer to [rpi 4b map](https://toptechboy.com/wp-content/uploads/2022/04/pinout-corrected-1024x605.jpg))
3. align the female gpio pins on the touchscreen to the male gpio pins on the raspberry pi towards the left.
4. connect the camera ribbon cable to the connector on the raspberry pi and do the same for the module.
5. plug in the usb-c to the power bank and the other side to the raspberry pi port.
6. connect the wired keyboard and mouse.
7. plug in the hdmi cable to the micro-usb adapter and plug the micro-usb to the raspberry pi.
### setup
8. download raspberry pi imager.
9. etch the latest version of raspbian onto the microsd card.
10. plug in the microsd card.
11. turn on the raspberry pi via the power bank.
12. go through the set up process.
13. open up the terminal and enter this command:
cloning the repository:
```
git clone https://github.com/johannlo2013/picamera.git
```
open up a new file called "init.sh" on Desktop:
```
nano ~/Desktop/init.sh
```
paste these three lines of code:
```
cd /
cd /home/mashedpotatoes/picamera/
python3 init.py
```
14. double-click "init.sh" on the desktop. 
15. select "execute in terminal".
16. take pictures and enjoy!
### how to use it
- click the wired button to snap a photo
- click the record button once to start and stop recording
- the exit button is self-explanatory
- click the time button 5 times to open the chromium browser (for students bringing cameras who want to watch youtube lol)