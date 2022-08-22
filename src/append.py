#!/usr/bin/python3




import datetime
import os
import re
import statistics
import unittest


class APPEND:
    def __init__(self, string, diff, rows, file):
        self.bufstring =string
        self.timediff = diff
        self.datarows = rows
        self.readfile = file
        self.datatext = 'datatext.txt'

    def appendata(self):
        ## section that appends new data to the main text datafile.
        # TO DO: Handle non-continous data files ie the RPi was not recording/appending data for x ammount of time or file 1 ends at 11:59:50 and File 2 does not have this time stamp but has 12:00:06.
        timestext =[]
        newfile = False
        #check if data file exists
        if os.path.exists(self.datatext):
            pass # append if already exists
        else:
            with open(self.datatext, 'wb') as t:        # make a new file if not
                print('Creating datatext.txt')
                newfile =True

        # Open datatext for text appending
        if not newfile:
            print('Searching datatext for matching time')
            with open(self.datatext, 'r') as datat:        #Open big data file
                lines = datat.readlines()
            for line in lines:
                if line.find('%') !=-1:
                    timestext.append(line[line.find('%'):(len(line)-1)])      #collect all the recorded
            last_rec_time_text = timestext[len(timestext)-1]                         # Save the latest time
            print('Last rec time is '+last_rec_time_text)


        ## Appending to text file, looks for most recent time and matches from the following time
        time_found = False
        notwriting = True
        padtimelist = []
        last_rec_diff = []
        last_date_time =[]
        if not newfile:
            try:
                datatextf = open(self.datatext,'a')
            except Exception as e3:
                print(str(e3))
            with open(self.readfile, 'r') as newf:
                newlines = newf.readlines()
            for newline in newlines:
                if notwriting:
                    if newline.find('%') !=-1 and time_found ==False:
                        var = newline[newline.find('%'):(len(newline)-1)]
                        if var == last_rec_time_text:
                            print('Time Found')
                            print(var)
                            print('Appending data to datatext.txt')
                            time_found = True
                    elif newline.find('%') !=-1 and time_found ==True:
                        notwriting = False
                        datatextf.write(newline)
                else:
                    datatextf.write(newline)
            datatextf.close()


            if not time_found:
                stamp = last_rec_time_text
                temp = (re.findall(r'\d+', stamp))
                try:
                    last_text_time = datetime.datetime(int(temp[0]),int(temp[1]),int(temp[2]),int(temp[3]),int(temp[4]),int(temp[5]))
                except Exception as e2:
                    struct = 'False'
                with open(self.readfile, 'r') as padded:
                    padlines = padded.readlines()
                    for padline in padlines:
                        if padline.find('%') !=-1:
                            padraw = (padline[padline.find('%'):(len(padline)-1)])
                            padtemp = (re.findall(r'\d+', padraw))
                            try:
                                struct = datetime.datetime(int(padtemp[0]),int(padtemp[1]),int(padtemp[2]),int(padtemp[3]),int(padtemp[4]),int(padtemp[5]))
                            except Exception as e2:
                                struct = 'False'
                            last_date_time.append(struct)
                    for idx, x in enumerate(last_date_time):
                        last_rec_diff.append((last_date_time[idx] - last_text_time).total_seconds())
                    padnum = min([n for n in last_rec_diff if n>0])
                    padindex = last_rec_diff.index(padnum)
                    padto = last_date_time[padindex]
                    if (padto - last_text_time)> datetime.timedelta(days =1):
                        print('Over 1 day since prevoius recorded data directly appending new data\n')
                        print('Copying all data to new file')
                        with open(self.readfile, 'r') as newf:
                            newlines = newf.readlines()
                        with open(self.datatext, 'a') as datatextf:
                            datatextf.write('######\n')
                            for line in newlines:
                                datatextf.write(line)
                    else:
                        with open(self.datatext, 'a') as datatextf:
                            print('Appending Large text file - Padding required between ' +last_text_time.strftime("%Y-%m-%d   %H:%M:%S")+ ' and ' + padto.strftime("%Y-%m-%d   %H:%M:%S") +'\n')
                            padcount =0
                            padding = True
                            writing = False
                            val = 1
                            while padding:
                                datatextf.write(self.bufstring)
                                if padcount == 0:
                                    printtime = last_text_time + datetime.timedelta(seconds = self.timediff*val)
                                    datatextf.write('\t% '+printtime.strftime("%Y-%m-%d   %H:%M:%S")+'\n')
                                else:
                                    datatextf.write('\n')
                                padnum -=1
                                padcount += 1
                                if padcount >(self.datarows):
                                    val +=1
                                    padcount = 0
                                if padnum == 0:
                                    padding = False
                            with open(self.readfile, 'r') as padded:
                                padlines = padded.readlines()
                                for padline in padlines:
                                    if padline.find('%') !=-1:
                                        stamp = padline[padline.find('%'):(len(padline)-1)]
                                        temp = (re.findall(r'\d+', stamp))
                                        if padindex == 0:
                                            struct = datetime.datetime(int(temp[0]),int(temp[1]),int(temp[2]),int(temp[3]),int(temp[4]),int(temp[5]))
                                            if writing == False and struct == padto:
                                                writing = True
                                        else:
                                            padindex -=1
                                    if writing:
                                        datatextf.write(padline)


        # if the large text file no longer exists
        if newfile:
            print('Copying all data to new file')
            with open(self.readfile, 'r') as newf:
                newlines = newf.readlines()
            with open(self.datatext, 'a') as datatextf:
                for line in newlines:
                    datatextf.write(line)

class TestAppend(unittest.TestCase):
    
    def test_new_datatext(self):
        string = '  00000  00000  00000  00000  00000  00000  00000  00000'
        diff = 16
        rows = 16
        file = 'Appendtest.txt'
        self.app=APPEND(string,diff,rows,file)
        self.app.datatext = 'testdatatext.txt'
        self.app.appendata()
        self.assertTrue(os.path.exists(self.app.datatext))
        self.assertGreater(os.path.getsize(self.app.datatext),0)
        os.remove('testdatatext.txt')

# The following tests all require specific setup with test files because they do not create a new file but modify an existing one. As such will be commented out for general testing
    '''
    def test_append_datatext(self):
        string = '  00000  00000  00000  00000  00000  00000  00000  00000'
        diff = 16
        rows = 16
        file = 'Appendtest.txt'
        self.app=APPEND(string,diff,rows,file)
        self.app.appendata()
        self.assertTrue(os.path.exists(self.app.datatext))
        self.assertGreater(os.path.getsize(self.app.datatext),0)
    
    def test_appendpad_datatext(self):
        string = '  00000  00000  00000  00000  00000  00000  00000  00000'
        diff = 16
        rows = 16
        file = 'Appendtestpad.txt'
        self.app=APPEND(string,diff,rows,file)
        self.app.appendata()
        self.assertTrue(os.path.exists(self.app.datatext))
        self.assertGreater(os.path.getsize(self.app.datatext),0)
    '''
