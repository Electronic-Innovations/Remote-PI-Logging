#!/usr/bin/python3

# Test script for 3-ch RPi Relay Board
import RPi.GPIO as GPIO
from time import sleep

# Relay channel definitions
relay1 = 26
relay2 = 20
relay3 = 21
# Initialise GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay1,GPIO.OUT)
# Relays are active-low
GPIO.output(relay1,True)

sleep(3)

print("Cycling relays")
# turns off EDM for aproximately 3 seconds
GPIO.output(relay1,False)
sleep(3)


GPIO.cleanup()
