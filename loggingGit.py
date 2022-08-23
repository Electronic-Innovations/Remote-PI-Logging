#!/usr/bin/python3

import datetime
import os

from src.readEDM import EDMSerial
from src.append import APPEND
from src.padding import PADDING


# get the current date time
now = datetime.datetime.now()
d1 = now.strftime("%Y-%m-%d__%H_%M")
filenametxt = '../../data_backup/'+d1+'.txt'
padfile = '../../data_pad/' + d1 + 'pad.txt'
datatext = '../../datatext.txt'

#create object for reading data in from the serial port
com = EDMSerial()
#Port will need to be changed for RPi
com.changePort('/dev/ttyUSB0')
#Get data from EDM and save to file
com.getEDMdata(filenametxt)

# create padding object
PAD = PADDING(filenametxt)

#Aquire time stamps from the data
times = PAD.mkTimeList()
#Derive time difference between page records and number of records per page
PAD.calcTimedif(times)
#Check fro missing records
PAD.checktimes(times)
#Prepare appropriate sring to pad the data
PAD.mkpadstring()
#Make Pad datafile
PAD.mkPaddata(padfile)


#Create Appending object for appending
APP = APPEND(PAD.padstring,PAD.time_difference,PAD.rows,padfile)
APP.datatext = datatext
APP.appendata()
