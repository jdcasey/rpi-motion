#!/usr/bin/env python3

import RPi.GPIO as gpio
import datetime
import time

gpio.setmode(gpio.BCM)
gpio.setup(23, gpio.IN)

try:
    time.sleep(2)
    while(True):
        if gpio.input(23):
            print("PING: " + str(datetime.datetime.now()))
            time.sleep(6)
        time.sleep(0.1)
except Exception as e:
    print(str(e))
    gpio.cleanup()


