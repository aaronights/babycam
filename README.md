# babycam
# Raspberry Pi Baby Monitor

I put together a project to make a video baby monitoring system. It's something that a parent would use to keep an eye on a resting child with a live video feed to a phone or tablet, and give notifications when the baby wakes or becomes restless.

For this project I opted to connect the Raspberry Pi to a standard network. Setting up WiFi can be done using terminal, but it's much simpler to connect an HDMI monitor and use the Raspbian desktop environment. Set up the Raspberry Pi to use a WiFi network like normal, with the networking icon in the task bar. To make it simpler to find the video stream later, right click on the icon and set the wireless interface to use a static IP address.

Crafting a case and mount for this project presents some challengers. It needed to be flexible to allow the camera to be positioned to get a good shot of the baby while it sleeps.

 
Like all of the camera modules, the NoIR camera connects to the Raspberry Pi with a 16mm wide ribbon cable. Initially I had the idea to put the camera on the end of a short flexible pole with the Pi in a case at its base. This had a problem - having a small thing sticking out that a baby could fit in its mouth isn't a good idea. I had to keep the unit big enough to not present a choking hazard. The best way to go about it was to integrate the camera and the Raspberry Pi together in a case and pivot the whole unit to get the correct angle.

 
I used a hinged plastic mount designed for attaching a GPS to a cars windscreen. Attached to this is an official Raspberry Pi 3 case, mounted upside down. I drilled a hole inside the lid of the case and used mounting tape to secure the camera module on the inside, letting the lens slightly poke out. The short ribbon cable flexed around to the socket on the Raspberry Pi. I also drilled holes and mounted two of these Infrared LED's in the lid. I combined them in series and added the appropriate resistor and used female jumper leads to connect them to the 5v terminal on the GPIO header. It can be a tight fit under the lid, so it is important to be careful that no leads touch any other pins or the main board of the Raspberry Pi.


The hinged mount is attached to a wall with adhesive picture frame pads - I didn't want to use suction cups as they can be unreliable for long term use. The case with the camera inside is then facing downward from the wall over a babies crib, and the hinge can be adjusted to get an optimal viewing angle.
 
To get the baby monitor system up and running I experimented with a few coding options. Python has extensive libraries for interfacing with both the standard and NoIR camera modules, including network streaming options. While coding for the camera in python is extensively customizable, I found that using the server socket transmission commands had significant latency issues when streaming an HD feed over a network. The camera can also be interfaced with by using standard Linux terminal commands and scripting. It's efficient for basic functionality, but isn't very well suited for a complex program like what is required for this project.

 
The solution I opted to use is the RPi Cam Web Interface suite. It is very flexible with configuration, but importantly it streams live video over a standard web interface - making it compatible with just about any smart device with a web browser. It also allows the Raspberry Pi to be shut down correctly with a button on the web interface. I didn't bother to put security on the video stream because it'll only be viewable on an encrypted WiFi network. The RPi Cam Web Interface does, however, support password prompt access and a range of permissions.
 

Before installation the camera needs to be enabled inside of Raspbian. Under Preferences in the main menu load the Raspberry Pi Configuration program and set the camera option to enable. With the camera enabled, installing the Interface software is done by pasting the following lines into a terminal window.


git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git  
cd RPi_Cam_Web_Interface  
chmod u+x *.sh  
./install.sh  
 

After that you'll see a dialog box with some options. Unless you have specific requirements, hit Enter to start the installation with the default settings. After it has rebooted accessing the software is done by entering the IP address of the Raspberry Pi into a browser. This can be done on the Pi itself or on any device connected to the same network.

Screen Interface

I played around with the video resolution, bitrate and framerate setting to get optimal performance over a wireless network. Devices like this are often placed far away from the router and through a few walls, so signal strength may not be the best.

Video res: 720x1280

I found the sweet spot in resolution to be 720p HD. Opposite to what is normal, I used a vertical 720x1280 video frame to fill the screen of a smart phone when used in portrait mode.

Video fps: 20

The default 25 frames per second is somewhat overkill for observing a baby that isn't moving very much while sleeping. Bumping the frame rate down to 20 still allows viewers to see if the baby is moving but slightly relaxes the demand it places on the wireless network.

Brightness: 60

Increasing the brightness does wash out the picture a little, but gives more clarity in low light.
Exposure Mode: nightpreview - The NoIR V2 is good in low light, but turning the exposure to nightpreview cleans up the image just a little more.

Image Quality: 100, Preview Quality: 100

Maxing out the image quality and preview quality didn't seem to have any impact on the streaming performance, but made the overall clarity just a little better. Setting the preview width to 720 allows the live video to be the full quality captured.

Motion detect mode: External

I changed the default on screen title to something a bit more appropriate - Baby Cam. I left the complete hours, minutes and seconds time stamp there. Having the seconds constantly counting gives a good indicator that the video feed is live and hasn't malfunctioned.


There are some settings I had to change manually outside of the web based UI, done by editing the file /etc/raspimjpeg.

Adding the line 'fullscreen true' to the bottom of the file. This makes the Index page of the camera interface default to full screen video, rather than showing the option buttons.
Changing the pre existing line motion_detection from false to true makes the system start motion detection automatically at boot.
 

Motion sensing
I implemented a system to send alerts when the baby starts to get restless during nap time. The RPi Cam Web Interface has integrated motion sensing algorithms that are well suited to detecting both subtle and more obvious motion. I tuned through trial and error and ended up with the following settings, configured under the 'Edit motion settings' button on the default index page.

On_event_start: python /etc/home/pi/alert.py 

When motion is detected the named python script will be executed to send out an alert.

Threshold: 2100

This is a tricky one. The motion detection sensitivity is defined by a number between 1 and 2147483647. Every use and scenario is different depending on the sensitivity required. Having the number too high results in it being triggered with no perceivable motion at all. 2100 seemed to work well for me.

Lightswtich: 55

Useful when the baby sleeps with the curtains slightly open on an overcast day. This option stops the sun moving out from behind clouds resulting in a false trigger due to the change in lighting.

Minimum_motion_frames: 3

The number of consecutive frames that motion needs to be present before the sensor is tripped. A baby doesn't move like The Flash, so having it a little higher than 1 gives less false triggers.
Under the schedule settings I cleared the boxes under Motion Start and Motion Stop. These are used when recording is to start when motion is detected. For a baby monitor a live alert is required, not a video recording.

 

Unfortunately the motion service can have complications when executing some commands. Searching around, I found that it was a bug that many users have encountered with no great solution. If you find that the alert script isn't executing, starting the motion program out of daemon mode from the command line makes it function properly. It's a work around rather than a solution, but it can be automatically done every time the Raspberry Pi boots. Edit bashrc via the command 'sudo nano .bashrc' and add the line 'motion -n' to the bottom of the file and the problem should be avoided.


Sending alerts
I used the on_motion_start parameter to trigger and execute a python script that sends out notifications. There is a range of different providers that offer applications on iOS and Android to receive notifications from inside a python script. I used Instapush, although other services work equally as well. Using it is done by signing up on their website, creating a new application then pasting the provided code with the unique appid and secret code parameters into a python script.

 

The Instapush API also needs to be installed on the Raspberry Pi, done simply with the following line in a terminal window.

sudo pip install instapush  
 

I placed this script in the default /home/pi directory and named it 'alert.py'.

```python
import RPi.GPIO as GPIO   
import time  
import os.path  
from instapush import Instapush, App  
GPIO.setmode(GPIO.BCM)    
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)    
  
input_state = GPIO.input(4)  
if input_state == False and os.path.isfile('active') == False:   
            open('active', 'a')  
            app = App(appid='xxxxxxxx', secret='xxxxxxxx')  
            app.notify(event_name='Baby_Monitor', trackers={ 'Baby': 'Louis'})  
            time.sleep(600)  
            os.remove('active')      
```            
            
* Lines 1 through 4 import the necessary modules for the script.
* Line 5 - 7 sets the numbering system for the GPIO pins on the Raspberry Pi, selects a pin number and sets it up for use as a switch trigger then gives it the variable 'input_state'.
* Line 8 is a if statement to check two conditions:
If the switch attached between GPIO pin 4 and a ground pin is active. I put a jumper to bridge pin 4 to the neighbouring ground pin. Removing the jumper disables the notifications from being sent.
If a file named 'active' is in the current directory. This is part of the method used to ensure that notifications are only sent once every 10 minutes to prevent a huge flood of alerts being sent consecutively.
* Line 9 creates a blank file titled 'active' in the current directory.
* Lines 10 and 11 are the Instapush provided code to trigger the sending of notifications.
* Line 12 waits for 600 seconds, or 10 minutes.
* Line 13 deletes the file 'active'.


The NoIR V2 camera is a great way to get clear images in low light situations, and the increased fidelity with the V2 makes for great quality images and videos. Outside of just monitoring sleeping babies, combining the Interface, the NoIR camera and a Raspberry Pi 3 together can make a very sophisticated security camera system. More than sending alerts, a relay could be added to the system to sound an alarm, turn the lights on in a room or lock a door with a solenoid. Nearly anything that a Raspberry Pi can do is able to be triggered by detecting motion. Plus the whole unit is smaller and cheaper yet higher fidelity than many commercial surveillance systems. Combining it with a big source of Infrared light, such as an array of LED's or a large bulb, the NoIR V2 camera could view a large area in absolute darkness.
 

If you have any questions about this project or the NoIR V2 in general, hit me up on Twitter - @aaronights.
