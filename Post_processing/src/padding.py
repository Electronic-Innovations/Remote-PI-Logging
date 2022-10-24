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
import os
class PADDING:
    def __init__(self, filenametxt):
        self.time_difference = 8
        self.rows = 8
        self.numberADCchannels =15
        self.filenametxt = filenametxt
        self.drows =[]
        self.diff_array =[]
        self.datetimelist =[]
        self.padstring = '  00000'
        self.pad =[]
        self.padfile = ''
    
    # Makes the padding string depending on the number of channels recorded
    def mkpadstring(self):
        for a in range(self.numberADCchannels-1):
            self.padstring +='  00000'


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
            elif count == 2 and started == True :
                self.numberADCchannels = round(len(line)/len(self.padstring))
            count +=1
        for items in newtimestext:
            if items is False:
                exit(-2)
        try:
            self.rows = (round(statistics.mean(self.drows)))
        except Exception as e1:
            pass
        return newtimestext

    def calcTimedif(self, timelist):
        temp =[]
        datelist = []
        diff_array =[]
        for idy, y in enumerate(timelist):
            temp.append(re.findall(r'\d+', timelist[idy]))
        for date in temp:
            try:
                struct = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(date[3]),int(date[4]),int(date[5]))
            except Exception as e3:
                struct = 'False'
            datelist.append(struct)
        for idx, x in enumerate(datelist):
            if idx ==0:
                continue
            if datelist[idx] == 'False' or datelist[idx-1] =='False':
                continue
            self.diff_array.append((datelist[idx]-datelist[idx-1]).seconds)
        self.time_difference = round(statistics.mean(self.diff_array))


    # Function used to compare each timestaped and determine where padding is required
    # Returns a list of list indicating how to pad the raw data where each list item has:
    # [start padding at time, for this many rows, skip this many timestamps, stop paddding at this time stamp]
    # For and Erased section of memroy the List looks like: ['Erased', num rows, recording start time]
    def checktimes(self,timelist):
        temppad = []
        pad = []
        skip = 0;
        temp =[]
        Erased = False
        for idy, y in enumerate(timelist):
            temp.append(re.findall(r'\d+', timelist[idy]))
        for date in temp:
            try:
                struct = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(date[3]),int(date[4]),int(date[5]))
            except Exception as e3:
                struct = 'False'
            self.datetimelist.append(struct)
        for idx, x in enumerate(self.datetimelist):
            if idx == 0:
                if self.datetimelist[idx] == 'False':
                    Erased = True
                    temppad.append('Erased')
                    temppad.append(self.time_difference)
                continue
            if Erased:
                if self.datetimelist[idx] == 'False':
                    temppad[1] += self.rows
                else:
                    Erased =False
                    temppad[1] += self.rows
                    temppad.append(self.datetimelist[idx+1])
                    self.pad.append(temppad)
                    temppad = []
                continue
            if self.datetimelist[idx] == 'False' and not Erased:
                skip += 1
                continue
            if skip == 0:
                diff = self.datetimelist[idx]-self.datetimelist[idx-1]
                if diff > datetime.timedelta(days =1):
                    self.pad = []
                    temppad.append('Start')
                    temppad.append(self.datetimelist[idx])
                    self.pad.append(temppad)
                    temppad =[]
                if diff.total_seconds() > self.time_difference + 1:
                    temppad.append(self.datetimelist[idx-1])
                    temppad.append(round((diff.total_seconds()/self.time_difference)*self.rows))
                    temppad.append(skip)
                    temppad.append(self.datetimelist[idx])
                    self.pad.append(temppad)
                    temppad = []
            if skip != 0:
                print('skip num: ' + str(skip))
                diff = self.datetimelist[idx]-self.datetimelist[idx-(1+skip)]
                if diff.total_seconds() > self.time_difference + 1:
                    temppad.append(self.datetimelist[idx-(1+skip)])
                    temppad.append(round((diff.total_seconds()/self.time_difference)*self.rows))
                    temppad.append(skip)
                    temppad.append(self.datetimelist[idx+1])
                    self.pad.append(temppad)
                    temppad = []
                skip = 0;
        if len(self.pad) == 0:
            self.pad = [['False']]





    def mkPaddata(self, padfile):
        index = 0
        done_padding =False
        self.padfile = padfile
        # No missing section or Erased data found copying straight to padfile
        if self.pad[0][0] == 'False':
            with open(self.filenametxt, 'r') as raw:
                lines = raw.readlines()
                with open(self.padfile, 'w') as padded:
                    for line in lines:
                        padded.write(line)
            done_padding = True
# Large Gap in data (>1 day) skipping to new data
        elif self.pad[0][0] == 'Start':
            starttime = self.pad[0][1]
            writing = False
            with open(self.padfile, 'w') as padded:
                with open(self.filenametxt, 'r') as raw:
                    lines = raw.readlines()
                    for line in lines:
                        if writing:
                            padded.write(line)
                            continue
                        if line.find('%') !=-1 and not writing:
                            stamp = line[line.find('%'):(len(line)-1)]
                            temp = (re.findall(r'\d+', stamp))
                            try:
                                struct = datetime.datetime(int(temp[0]),int(temp[1]),int(temp[2]),int(temp[3]),int(temp[4]),int(temp[5]))
                            except Exception as e2:
                                struct = 'False'
                            if struct == 'False':
                                pass
                            elif struct == starttime:
                                writing = True
                                padded.write(line)
            index = 1
            

        # Erased data found padding file and adding time stamps retrocatively from oldest recorded time
        elif self.pad[0][0] == 'Erased':
            starttime = self.pad[0][2] - datetime.timedelta(seconds = self.pad[0][1])
            padding = True
            writing = False
            index =1
            padnum = self.pad[0][1]
            padcount = 0
            val = 0
            with open(self.padfile, 'w') as padded:
                with open(self.filenametxt, 'r') as raw:
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
                            elif struct == self.pad[0][2]:
                                while padding:
                                    padded.write(self.padstring)
                                    if padcount == 0:
                                        printtime = starttime + datetime.timedelta(seconds = self.time_difference*val)
                                        padded.write('\t% '+printtime.strftime("%Y-%m-%d   %H:%M:%S")+'\n')
                                    else:
                                        padded.write('\n')
                                    padnum -=1
                                    padcount += 1
                                    if padcount >(self.rows-1):
                                        val +=1
                                        padcount = 0
                                    if padnum == 0:
                                        padding = False
                                writing = True
                                padded.write(line)
                        elif padding:
                            padded.write(self.padstring)
                            if padcount == 0:
                                printtime = starttime + datetime.timedelta(seconds = self.time_difference*val)
                                padded.write('\t% '+printtime.strftime("%Y-%m-%d   %H:%M:%S")+'\n')
                            else:
                                padded.write('\n')
                            padnum -=1
                            padcount += 1
                            if padcount >self.rows-1:
                                val +=1
                                padcount = 0
                            if padnum == 0:
                                pass
                                #padding = False
                                #writing = True
            try:
                test = self.pad[index]
            except Exception as e4:
                done_padding = True
                        

        # Other forms of time stamp mismatch, (EDM was not recording for x time) padding out the length and time stamps of the file to make it continous
        if index == 0 or done_padding == False:
            if not os.path.exists(self.padfile):
                with open(self.padfile,'w') as make:
                    pass
            padcount =0
            padding = False
            skip = 0
            val = 0
            with open(self.filenametxt, 'r') as raw:
                if index == 0:
                    writing = True
                    lines = raw.readlines()
                with open(self.padfile, 'r+') as padded:
                    if index != 0:
                        writing = False
                        lines = padded.readlines()
                        padded.seek(0)
                    for line in lines:
                        if line.find('%') !=-1:
                            stamp = line[line.find('%'):(len(line)-1)]
                            temp = (re.findall(r'\d+', stamp))
                            if skip == 0:
                                try:
                                    struct = datetime.datetime(int(temp[0]),int(temp[1]),int(temp[2]),int(temp[3]),int(temp[4]),int(temp[5]))
                                except Exception as e2:
                                    struct = 'False'
                                if struct == 'False':
                                    writing = False
                                    continue
                                else:
                                    writing = True
                                if writing == False and struct == skipto:
                                    writing = True
                                for idx in range(0,len(self.pad)):
                                    if idx == 0 and (self.pad[0][0]=='False' or self.pad[0][0]=='Erased' or self.pad[0][0]=='Start'):
                                        continue
                                    if struct == self.pad[idx][0]:
                                        padding = True
                                        writing = False
                                        skip = self.pad[idx][2]
                                        skipto = self.pad[idx][3]
                                        padnum = self.pad[idx][1]
                                        break
                            else:
                                skip -=1
                        while padding:
                            padded.write(self.padstring)
                            if padcount == 0:
                                printtime = struct + datetime.timedelta(seconds = self.time_difference*val)
                                padded.write('\t% '+printtime.strftime("%Y-%m-%d   %H:%M:%S")+'\n')
                            else:
                                padded.write('\n')
                            padnum -=1
                            padcount += 1
                            if padcount >(self.rows-1):
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
    
    def test_data_column(self):
        list = PADDING.mkTimeList(self.PAD)
        self.assertEqual(self.PAD.numberADCchannels,15)

    def test_row_avg(self):
        list = PADDING.mkTimeList(self.PAD)
        self.assertEqual(self.PAD.rows,8)

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

class Testchecktimes(unittest.TestCase):
    
    def test_erased_padlist(self):
        self.PAD = PADDING('2022-08-15__08_00test.txt')
        temp =PADDING.mkTimeList(self.PAD)
        self.PAD.calcTimedif(temp)
        self.PAD.checktimes(temp)
        self.assertEqual(self.PAD.pad[0][0],'Erased')

    def test_pad_padlist(self):
        self.PAD = PADDING('2022-08-15__08_00skip.txt')
        temp =PADDING.mkTimeList(self.PAD)
        self.PAD.calcTimedif(temp)
        self.PAD.checktimes(temp)
        self.assertEqual(self.PAD.pad[0][0],datetime.datetime(2022,8,15,16,17,50))
        self.assertEqual(self.PAD.pad[0][1],60)
        self.assertEqual(self.PAD.pad[0][2],0)
        self.assertEqual(self.PAD.pad[0][3],datetime.datetime(2022,8,15,16,18,54))

    def test_old_data_padlist(self):
        self.PAD = PADDING('2022-08-15__08_00old.txt')
        temp =PADDING.mkTimeList(self.PAD)
        self.PAD.calcTimedif(temp)
        self.PAD.checktimes(temp)
        self.assertEqual(self.PAD.pad[0][1],datetime.datetime(2022,8,17,16,58,55))
        self.assertEqual(self.PAD.pad[0][0],'Start')

    def test_erased_pad(self):
        self.PAD = PADDING('2022-08-15__08_00test.txt')
        temp =PADDING.mkTimeList(self.PAD)
        self.PAD.calcTimedif(temp)
        self.PAD.checktimes(temp)
        self.assertEqual(self.PAD.pad[0][0],'Erased')
        self.assertEqual(self.PAD.pad[1][0],datetime.datetime(2022,8,15,16,43,58))
        self.assertEqual(self.PAD.pad[1][1],81)
        self.assertEqual(self.PAD.pad[1][2],0)
        self.assertEqual(self.PAD.pad[1][3],datetime.datetime(2022,8,15,16,45,19))

    def test_erased_old(self):
        self.PAD = PADDING('2022-08-15__08_00terasedold.txt')
        temp =PADDING.mkTimeList(self.PAD)
        self.PAD.calcTimedif(temp)
        self.PAD.checktimes(temp)
        self.assertEqual(self.PAD.pad[0][1],datetime.datetime(2022,8,17,16,58,55))
        self.assertEqual(self.PAD.pad[0][0],'Start')

    def test_pad_old(self):
        self.PAD = PADDING('2022-08-15__08_00old.txt')
        temp =PADDING.mkTimeList(self.PAD)
        self.PAD.calcTimedif(temp)
        self.PAD.checktimes(temp)
        self.assertEqual(self.PAD.pad[0][1],datetime.datetime(2022,8,17,16,58,55))
        self.assertEqual(self.PAD.pad[0][0],'Start')

    def test_old_pad(self):
        self.PAD = PADDING('2022-08-15__08_00oldskip.txt')
        temp =PADDING.mkTimeList(self.PAD)
        self.PAD.calcTimedif(temp)
        self.PAD.checktimes(temp)
        self.assertEqual(self.PAD.pad[0][1],datetime.datetime(2022,8,17,16,58,55))
        self.assertEqual(self.PAD.pad[0][0],'Start')
        self.assertEqual(self.PAD.pad[2][0],datetime.datetime(2022,8,17,16,58,55))
        self.assertEqual(self.PAD.pad[2][1],45)
        self.assertEqual(self.PAD.pad[2][2],0)
        self.assertEqual(self.PAD.pad[2][3],datetime.datetime(2022,8,17,16,59,43))

# Note that these test only asses the size of files not nessicarily their contents
class Testfilepadding(unittest.TestCase):
    
    def test_erased_file(self):
        self.PAD = PADDING('2022-08-15__08_00testE.txt')
        temp =PADDING.mkTimeList(self.PAD)
        self.PAD.calcTimedif(temp)
        self.PAD.checktimes(temp)
        self.PAD.mkpadstring()
        self.PAD.mkPaddata('2022-08-15__08_00testEpad.txt')
        self.assertGreater(os.path.getsize('2022-08-15__08_00testE.txt'), os.path.getsize('2022-08-15__08_00testEpad.txt'))
        os.remove('2022-08-15__08_00testEpad.txt')

    def test_skip_file(self):
        self.PAD = PADDING('2022-08-15__08_00skip.txt')
        temp =PADDING.mkTimeList(self.PAD)
        self.PAD.calcTimedif(temp)
        self.PAD.checktimes(temp)
        self.PAD.mkpadstring()
        self.PAD.mkPaddata('2022-08-15__08_00skipPad.txt')
        self.assertGreater(os.path.getsize('2022-08-15__08_00skipPad.txt'),os.path.getsize('2022-08-15__08_00skip.txt'))
        os.remove('2022-08-15__08_00skipPad.txt')
        
    def test_skip2_file(self):
        self.PAD = PADDING('2022-08-15__08_00skip2.txt')
        temp =PADDING.mkTimeList(self.PAD)
        self.PAD.calcTimedif(temp)
        self.PAD.checktimes(temp)
        self.PAD.mkpadstring()
        self.PAD.mkPaddata('2022-08-15__08_00skip2Pad.txt')
        self.assertGreater(os.path.getsize('2022-08-15__08_00skip2Pad.txt'),os.path.getsize('2022-08-15__08_00skip2.txt'))
        os.remove('2022-08-15__08_00skip2Pad.txt')

    def test_olddata_file(self):
        self.PAD = PADDING('2022-08-15__08_00old.txt')
        temp =PADDING.mkTimeList(self.PAD)
        self.PAD.calcTimedif(temp)
        self.PAD.checktimes(temp)
        self.PAD.mkpadstring()
        self.PAD.mkPaddata('2022-08-15__08_00oldPad.txt')
        self.assertGreater(os.path.getsize('2022-08-15__08_00old.txt'),os.path.getsize('2022-08-15__08_00oldPad.txt'))
        os.remove('2022-08-15__08_00oldPad.txt')
