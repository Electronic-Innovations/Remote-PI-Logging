#!/usr/bin/python3

'''
This program is wriiten to automatically clean the memory of the RPi so that it does not fill up
It will remove the oldest files indicated by ther filenames untill there is 2GB of free space. The datatext.txt file will need to be cleared mannualy.
'''

import shutil
import glob
import datetime
import os

print((datetime.datetime.now()).strftime("%Y-%m-%d__%H_%M"))
#Get the amount of free space in the filesystem
total, used, free = shutil.disk_usage('/home/pi/data_backup')
freeGB = free/1024/1024/1024
#freeGB = 1
print(str(freeGB) + " Gb of Free Space")
#if less than 2GB do a clean up
if (freeGB<2):
    print("Less than 2Gb removing files to ensure 2Gb of space")
    #Aquire all the files in the data_backup and data_pad directory and sort they alphabetically
    #files = sorted(glob.glob("dummy/*.txt"))
    #files2 = sorted(glob.glob("dummypad/*.txt"))
    files = sorted(glob.glob("/home/pi/data_backup/*.txt"))
    files2 = sorted(glob.glob("/home/pi/data_pad/*.txt"))
    #Get current time
    now = datetime.datetime.now()
    # Loop over each file and removed one at a time checking storage space each time
    if len(files)>= len(files2):
        num = len(files)
    else:
        num = len(files2)
    for i in range(num):
        # remove oldest backup file
        if os.path.isfile(files[i]):
            print("Removing:" + files[i])
            os.remove(files[i])
            #freeGB = freeGB +0.5
        else:    ## Show an error ##
            print("Error: file not found:" + files[i])
        #Check freed space
        total, used, free = shutil.disk_usage('/home/pi/data_backup')
        freeGB = free/1024/1024/1024
        if freeGB>2:
            break
        
        # remove oldest padfile
        if os.path.isfile(files2[i]):
            print("Removing:" + files2[i])
            os.remove(files2[i])
            #freeGB = freeGB +0.5
        else:    ## Show an error ##
            print("Error: file not found:" + files2[i])
        total, used, free = shutil.disk_usage('/home/pi/data_backup')
        freeGB = free/1024/1024/1024
        if freeGB>2:
            break
quit()

