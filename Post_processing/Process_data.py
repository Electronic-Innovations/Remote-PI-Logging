#!/usr/bin/python3
'''
This script operates to pad and conctenate data files from the EDM recorded by the RPi. It utilises the same scripts and methods as the LoggingGit.py program. These scripst are contained the the src folder.

USAGE
To use this script paste this file and the acompaning src folder into the directory containing the datafiles to be merged. This progran expects the files to be .txt files and named such "YYYY-mm-dd__HH_MM.txt". Running this program in the directory using

python3 Process_data.py

Will generate a text file named with the first data file and lest data file in its name conatning the megerd, padded and concatinated data.
It does expect all the data to be in a consistent format.
'''



import datetime
import os
import glob
import time
from src.append import APPEND
from src.padding import PADDING


# get the current date time
now = datetime.datetime.now()
d1 = now.strftime("%Y-%m-%d__%H_%M")
#filenametxt = 'data_backup/'+d1+'.txt'
#padfile = 'data_pad/' + d1 + 'pad.txt'


#get an ordered list of filenames form the current directory
filelist = sorted(glob.glob('*.txt'))
datatext = filelist[0] + '___' + filelist[len(filelist)-1]
print(datatext)

#check if data file exists
if os.path.exists(datatext):
    pass # append if already exists
else:
    with open(datatext, 'wb') as t:        # make a new file if not
        print('Creating' + datatext)

with open(datatext, 'a') as writedata:
    print('Copying all data to new file')
    with open(filelist[0], 'r') as newf:
        newlines = newf.readlines()
        for line in newlines:
            writedata.write(line)
# Iterate through the different files and match the times and append new data to the main datatext file
for i in range(1,len(filelist)):

    # create padding object
    PAD = PADDING(filelist[i])

    #Aquire time stamps from the data
    times = PAD.mkTimeList()
    #Derive time difference between page records and number of records per page
    PAD.calcTimedif(times)
    #Check fro missing records
    PAD.checktimes(times)
    #Prepare appropriate sring to pad the data
    PAD.mkpadstring()
    padfile = 'pad'+filelist[i]
    #Make Pad datafile
    PAD.mkPaddata(padfile)


    #Create Appending object for appending
    APP = APPEND(PAD.padstring,PAD.time_difference,PAD.rows,padfile)
    APP.datatext = datatext
    APP.appendata()

# Remove excess files from the system, can be commented out for debugging.
padlist = sorted(glob.glob('pad*.txt'))
for i in range(0,len(padlist)):
    os.remove(padlist[i])

