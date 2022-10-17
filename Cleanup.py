#!/usr/bin/python3

'''
This program is wriiten to automatically clean the memory of the RPi so that it does not fill up
It will remove data that is older than (INSERT TIME) than the current time from the data_backup and data_pad directories. The datatext.txt file will need to be cleared mannualy.
'''

import shutil
import glob
import datetime
import os
# delete data older than
days = 60
#total, used, free = shutil.disk_usage('/home/pi/data_backup')
#freeGB = free/1024/1024/1024
freeGB = 1
if (freeGB<2):
    #files = glob.glob("dummy/*.txt")
    files = glob.glob("/home/pi/data_backup/*.txt")
    now = datetime.datetime.now()
    for file in files:
        date_string = file.replace('.txt','')
        #date_string = date_string.replace('dummy/','')
        date_string = date_string.replace('/home/pi/data_backup/','')
        file_date = datetime.datetime.strptime(date_string,'%Y-%m-%d__%H_%M')
        difference = now - file_date
        if(difference> datetime.timedelta(days = days)):
            if os.path.isfile(file):
                print("Removing:" + file)
                os.remove(file)
            else:    ## Show an error ##
                print("Error: %s file not found" % file)
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
                print("Error: %s file not found" % file2)
    
    
