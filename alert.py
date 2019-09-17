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