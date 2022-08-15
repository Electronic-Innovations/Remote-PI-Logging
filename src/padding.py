'''
Contains functions for creadting a padded .txt file where required.

mkTimeList
    creates a list of strings containg all the timestamps in the raw data

checktimes
    looks at a list of timestamps and uses the pre-defined time_difference to determine if they have any anomalies. Creates a structured list of lits to pass information as to how to pad the data to make it continous.
    
mkPaddata
    Uses the padlist provided from checktimes to create a padded data file (if required)
'''




import datetime
import re
import statistics
import unittest

class PADDING:
    def __init__(self, filenametxt):
        self.time_difference = 8
        self.rows = 8
        self.filenametxt = filenametxt
        self.drows =[]
        self.diff_array =[]
    # Collectes all the time stamps in the data
    def mkTimeList(self):
        newtimestext =[]
        drows = []
        with open(self.filenametxt, 'r') as raw:
            lines = raw.readlines()
            count = 0
            started = False
        for line in lines:
            if line.find('%') !=-1:
                newtimestext.append(line[line.find('%'):(len(line)-1)])
                self.drows.append(count)
                count = 0
                started = True
            count +=1
        for items in newtimestext:
            if items is False:
                exit(-2)
        try:
            self.rows = (round(statistics.mean(drows)))
        except Exception as e1:
            pass
        return newtimestext

    def calcTimedif(self, timelist):
        temp =[]
        datetimelist = []
        diff_array =[]
        for idy, y in enumerate(timelist):
            temp.append(re.findall(r'\d+', timelist[idy]))
        for date in temp:
            try:
                struct = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(date[3]),int(date[4]),int(date[5]))
            except Exception as e3:
                struct = 'False'
            datetimelist.append(struct)
        for idx, x in enumerate(datetimelist):
            if idx ==0:
                continue
            if datetimelist[idx] == 'False' or datetimelist[idx-1] =='False':
                continue
            self.diff_array.append((datetimelist[idx]-datetimelist[idx-1]).seconds)
        self.time_difference = round(statistics.mean(self.diff_array))


    # Function used to compare each timestaped and determine where padding is required
    # Returns a list of list indicating how to pad the raw data where each list item has:
    # [start padding at time, for this many rows, skip this many timestamps, stop paddding at this time stamp]
    # For and Erased section of memroy the List looks like: ['Erased', num rows, recording start time]
    def checktimes(self,timelist, time_difference):
        temppad = []
        pad = []
        skip = 0;
        temp =[]
        datetimelist = []
        Erased = False
        for idy, y in enumerate(timelist):
            temp.append(re.findall(r'\d+', timelist[idy]))
        for date in temp:
            try:
                struct = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(date[3]),int(date[4]),int(date[5]))
            except Exception as e3:
                struct = 'False'
            datetimelist.append(struct)
        for idx, x in enumerate(datetimelist):
            if idx == 0:
                if datetimelist[idx] == 'False':
                    Erased = True
                    temppad.append('Erased')
                    temppad.append(time_difference)
                continue
            if Erased:
                if datetimelist[idx] == 'False':
                    temppad[1] += time_difference
                else:
                    Erased =False
                    temppad[1] += time_difference
                    temppad.append(datetimelist[idx+1])
                    pad.append(temppad)
                    temppad = []
                continue
            if datetimelist[idx] == 'False' and not Erased:
                skip += 1
                continue
            if skip == 0:
                diff = datetimelist[idx]-datetimelist[idx-1]
                if diff.total_seconds() > time_difference + 1:
                    temppad.append(datetimelist[idx-1])
                    temppad.append(diff.total_seconds())
                    temppad.append(skip)
                    temppad.append(datetimelist[idx])
                    pad.append(temppad)
                    temppad = []
            if skip != 0:
                print('skip num: ' + str(skip))
                diff = datetimelist[idx]-datetimelist[idx-(1+skip)]
                if diff.total_seconds() > time_difference + 1:
                    temppad.append(datetimelist[idx-(1+skip)])
                    temppad.append(diff.total_seconds())
                    temppad.append(skip)
                    temppad.append(datetimelist[idx+1])
                    pad.append(temppad)
                    temppad = []
                skip = 0;
        if len(pad) == 0:
            pad = [['False']]
        return pad





    def mkPaddata(self,filenametxt, padfile, padlist, time_difference):
        # No missing section or Erased data found copying straight to padfile
        if padlist[0][0] == 'False':
            with open(filenametxt, 'r') as raw:
                lines = raw.readlines()
                with open(padfile, 'w') as padded:
                    for line in lines:
                        padded.write(line)
        # Erased data found padding file and adding time stamps retrocatively from oldest recorded time
        elif padlist[0][0] == 'Erased':
            starttime = padlist[0][2] - datetime.timedelta(seconds = padlist[0][1])
            padding = True
            writing = False
            padnum = padlist[0][1]
            padcount = 0
            val = 0
            with open(padfile, 'w') as padded:
                with open(filenametxt, 'r') as raw:
                    lines = raw.readlines()
                    for line in lines:
                        if writing:
                            padded.write(line)
                        if line.find('%') !=-1 and not writing:
                            stamp = line[line.find('%'):(len(line)-1)]
                            temp = (re.findall(r'\d+', stamp))
                            try:
                                struct = datetime.datetime(int(temp[0]),int(temp[1]),int(temp[2]),int(temp[3]),int(temp[4]),int(temp[5]))
                            except Exception as e2:
                                struct = 'False'
                            if struct == 'False':
                                pass
                            elif struct == padlist[0][2]:
                                while padding:
                                    padded.write(padstring)
                                    if padcount == 0:
                                        printtime = starttime + datetime.timedelta(seconds = time_difference*val)
                                        padded.write('\t% '+printtime.strftime("%Y-%m-%d   %H:%M:%S")+'\n')
                                    else:
                                        padded.write('\n')
                                    padnum -=1
                                    padcount += 1
                                    if padcount >(time_difference-1):
                                        val +=1
                                        padcount = 0
                                    if padnum == 0:
                                        padding = False
                                writing = True
                                padded.write(line)
                        elif padding:
                            padded.write(padstring)
                            if padcount == 0:
                                printtime = starttime + datetime.timedelta(seconds = time_difference*val)
                                padded.write('\t% '+printtime.strftime("%Y-%m-%d   %H:%M:%S")+'\n')
                            else:
                                padded.write('\n')
                            padnum -=1
                            padcount += 1
                            if padcount >7:
                                val +=1
                                padcount = 0
                            if padnum == 0:
                                pass
                                #padding = False
                                #writing = True
                        


        # Other forms of time stamp mismatch, (EDM was not recording for x time) padding out the length and time stamps of the file to make it continous
        else:
            padcount =0
            padding = False
            skip = 0
            writing = True
            val = 0
            with open(filenametxt, 'r') as raw:
                lines = raw.readlines()
                with open(padfile, 'w') as padded:
                    for line in lines:
                        if line.find('%') !=-1:
                            stamp = line[line.find('%'):(len(line)-1)]
                            temp = (re.findall(r'\d+', stamp))
                            if skip == 0:
                                struct = datetime.datetime(int(temp[0]),int(temp[1]),int(temp[2]),int(temp[3]),int(temp[4]),int(temp[5]))
                                if writing == False and struct == skipto:
                                    writing = True
                                for idx, x in enumerate(padlist):
                                    if struct == padlist[idx][0]:
                                        padding = True
                                        writing = False
                                        skip = padlist[idx][2]
                                        skipto = padlist[idx][3]
                                        padnum = padlist[idx][1] + 8
                                        
                                        break
                            else:
                                skip -=1
                        while padding:
                            padded.write(padstring)
                            if padcount == 0:
                                printtime = struct + datetime.timedelta(seconds = time_difference*val)
                                padded.write('\t% '+printtime.strftime("%Y-%m-%d   %H:%M:%S")+'\n')
                            else:
                                padded.write('\n')
                            padnum -=1
                            padcount += 1
                            if padcount >(time_difference-1):
                                val +=1
                                padcount = 0
                            if padnum == 0:
                                padding = False
                        if writing:
                            padded.write(line)
                            padcount =0
                            val =0



class TestTimeList(unittest.TestCase):

    def setUp(self):
        self.PAD = PADDING('test.txt')


    def test_list_times(self):
        list = PADDING.mkTimeList(self.PAD)
        for items in list:
            self.assertTrue(items)
    
    def test_empty_file(self):
        self.PAD.filenametxt = 'empty.txt'
        list = PADDING.mkTimeList(self.PAD)
        for items in list:
            self.assertFalse(items)

    def test_row_count(self):
        self.PAD.filenametxt = 'rowtest.txt'
        list = PADDING.mkTimeList(self.PAD)
        self.assertAlmostEqual(self.PAD.drows[0],3)
        self.assertAlmostEqual(self.PAD.drows[1],8)
        self.assertAlmostEqual(self.PAD.drows[2],6)
        self.assertAlmostEqual(self.PAD.drows[3],8)
        self.assertAlmostEqual(self.PAD.drows[4],10)

    def test_row_avg(self):
        list = PADDING.mkTimeList(self.PAD)
        self.assertIs(self.PAD.rows,8)

class TestcheckTimediff(unittest.TestCase):
    
    def setUp(self):
        self.PAD = PADDING('test.txt')
        
    def test_diff_array(self):
        self.PAD.calcTimedif(PADDING.mkTimeList(self.PAD))
        self.assertIsInstance(self.PAD.diff_array[0],int)
    def test_diff_array_average(self):
        self.PAD.time_difference=0
        self.PAD.calcTimedif(PADDING.mkTimeList(self.PAD))
        self.assertEqual(self.PAD.time_difference,8)
