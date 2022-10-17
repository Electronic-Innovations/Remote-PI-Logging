#!/usr/bin/python3

'''
This program is wriiten to automatically clean the memory of the RPi so that it does not fill up
It will remove data that is older than 60 days than the current time from the data_backup and data_pad directories. The datatext.txt file will need to be cleared mannualy.
'''

import shutil
import glob
import datetime
import os
# remove data older than
days = 60

#Get the amount of free space in the filesystem
total, used, free = shutil.disk_usage('/home/pi/data_backup')
freeGB = free/1024/1024/1024
print(freeGB + " Gb of Free Space")
#freeGB = 1
print(datetime.datetime.strftime(datetime.datetime.now()))
#if less than 2GB do a clean up
if (freeGB<2):
    print("Less than 2Gb removing files oflder than "+days+" days")
    #Aquire all the files in the data_backup directory
    #files = glob.glob("dummy/*.txt")
    files = glob.glob("/home/pi/data_backup/*.txt")
    #Get current time
    now = datetime.datetime.now()
    # Loop over each file and strip path and .txt, check the filename for datetime of creation
    for file in files:
        date_string = file.replace('.txt','')
        #date_string = date_string.replace('dummy/','')
        date_string = date_string.replace('/home/pi/data_backup/','')
        file_date = datetime.datetime.strptime(date_string,'%Y-%m-%d__%H_%M')
        difference = now - file_date
        # Compare to see if the file is old enough to be deleted if so delete file
        if(difference> datetime.timedelta(days = days)):
            if os.path.isfile(file):
                print("Removing:" + file)
                os.remove(file)
            else:    ## Show an error ##
                print("Error: file not found:" + file)
    
    # Same process but in the data_pad directory
    #files2 = glob.glob("dummy/*.txt")
    files2 = glob.glob("/home/pi/data_pad/*.txt")
    for file2 in files2:
        date_string = file2.replace('pad.txt','')
        #date_string = date_string.replace('dummy/','')
        date_string = date_string.replace('/home/pi/data_pad/','')
        file_date = datetime.datetime.strptime(date_string,'%Y-%m-%d__%H_%M')
        difference = now - file_date
        if(difference> datetime.timedelta(days = days)):
            if os.path.isfile(file2):
                print("Removing:" + file2)
                os.remove(file2)
            else:    ## Show an error ##
                print("Error: file not found" + file2)
else:
    print("Over 2Gb of space remaning not removing files")
    
