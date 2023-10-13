#!/usr/bin/python3

import datetime
import os

from src.readEDM import EDMSerial
from src.append import APPEND
from src.padding import PADDING

# get the current date time
now = datetime.datetime.now()
d1 = now.strftime("%Y-%m-%d__%H_%M")
filenametxt = 'jgrab/'+d1+'.txt'

#create object for reading data in from the serial port
com = EDMSerial()
#Port will need to be changed for RPi
com.changePort('/dev/ttyUSB0')
#Get data from EDM and save to file
com.commandEDMdata(filenametxt,'JGRAB')
