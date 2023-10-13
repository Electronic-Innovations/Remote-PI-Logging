'''
Module for probing the EDM to output all of its memory and directly copy this output to the provided text file
Defaults to port '/dev/ttyUSB0'
'''

import unittest
import serial
import timeit
import os

class EDMSerial:
    def __init__(self,port='/dev/ttyUSB0'):
        self.port = port
        
        
    def changePort(self,port):
        self.port = port
        
        
    def getEDMdata(self,filenametxt):
        data_in_buffer =True
        ok_num =0
        opened_port =False
        # Open a serial Port
        com = serial.Serial()
        com.baudrate = 57600
        com.port = self.port
        #com.port = '/dev/ttyUSB0'
        com.exclusive = True
        com.timeout = 180
        com.xonxoff = True
        print(com.isOpen())
        if com.isOpen() is True:
            print("Serial port is in use not recording data")
            exit(-1)
        try:
            com.open()
        except Exception as e2:
            print("Failed to open Serial port \nCheck it is not opened elsewhere")
            print(str(e2))
            exit(-2)
        else:
            print("serial port opened")


        #open a text file to log data
        try:
            if filenametxt == 'create_new_text_test.txt':
                test = open(filenametxt, 'wb')
                test.close
                exit(1)
            txt = open(filenametxt,'wb')

        except Exception as e3:
            print(str(e3))
            exit(-2)
        try:
            #start timer to ensure the program doesn't get stuck
            tic=timeit.default_timer()
            print("writing to EDM: 'd 24 5 * 60 M* -SSPRD'")
            # clear the stack for the EDM
            send = ' ..\r'
            com.write(send.encode())
            # Send command to print logged data
            send = 'd 24 5 * 60 M* -SSPRD\r'
            com.write(send.encode())
            # while there is data in the buffer echo it back to the terminal
            
            while data_in_buffer:
                data = com.read_until(b'\r\n')
                data = data.decode('ascii', 'ignore')
                data = data.replace('\x11','')        #Ignore unknown Ascii characters
                txt.write(data.encode('ascii'))
                if data.find('ok') == -1:
                    toc = timeit.default_timer();
                    if(toc-tic)>900:
                        data_in_buffer = False
                        print('Serial Port Timeout over 15 minutes to recieve all data')
                    pass
                else:
                    #time.sleep(2)
                    ok_num= ok_num+1
                    if ok_num ==2:
                        data_in_buffer =False
                        print('Buffer is empty\n')
            txt.close()
            com.close()
        except Exception as e1:
            print("error in comminucations \n" + str(e1))
            txt.close()
            com.close()
            raise

    def getEDMdata_INTS(self,filenametxt):
        data_in_buffer =True
        ok_num =0
        opened_port =False
        # Open a serial Port
        com = serial.Serial()
        com.baudrate = 57600
        com.port = self.port
        #com.port = '/dev/ttyUSB0'
        com.exclusive = True
        com.timeout = 180
        com.xonxoff = True
        print(com.isOpen())
        if com.isOpen() is True:
            print("Serial port is in use not recording data")
            exit(-1)
        try:
            com.open()
        except Exception as e2:
            print("Failed to open Serial port \nCheck it is not opened elsewhere")
            print(str(e2))
            exit(-2)
        else:
            print("serial port opened")


        #open a text file to log data
        try:
            if filenametxt == 'create_new_text_test.txt':
                test = open(filenametxt, 'wb')
                test.close
                exit(1)
            txt = open(filenametxt,'wb')

        except Exception as e3:
            print(str(e3))
            exit(-2)
        try:
            #start timer to ensure the program doesn't get stuck
            tic=timeit.default_timer()
            print("writing to EDM: '\n: INST_02\n0 INSTBUFFADR  source^[ 0 ]!\n2 INSTBUFFADR  source^[ 1 ]!\n2 slog_fields C!\ninstantaneous SLOG\nd 100 50 M* -STOPSLOG\nd 333 MS\nd 100 50 M* -SSPRD\nRESET\n;'")
            # clear the stack for the EDM
            send = ' ..\r'
            com.write(send.encode())
            send = ': INST_02\r0 INSTBUFFADR  source^[ 0 ]!\r2 INSTBUFFADR  source^[ 1 ]!\r2 slog_fields C!\rinstantaneous SLOG\rd 100 50 M* -STOPSLOG\rd 333 MS\rd 100 50 M* -SSPRD\rRESET\r;\r'
            com.write(send.encode())
            # Send command to print logged data
            send = 'INST_02\r'
            com.write(send.encode())
            # while there is data in the buffer echo it back to the terminal
            
            while data_in_buffer:
                data = com.read_until(b'\r\n')
                data = data.decode('ascii', 'ignore')
                data = data.replace('\x11','')        #Ignore unknown Ascii characters
                txt.write(data.encode('ascii'))
                if data.find('ok') == -1:
                    toc = timeit.default_timer();
                    if(toc-tic)>900:
                        data_in_buffer = False
                        print('Serial Port Timeout over 15 minutes to recieve all data')
                    pass
                else:
                    #time.sleep(2)
                    ok_num= ok_num+1
                    if ok_num ==2:
                        data_in_buffer =False
                        print('Buffer is empty\n')
            txt.close()
            com.close()
        except Exception as e1:
            print("error in comminucations \n" + str(e1))
            txt.close()
            com.close()
            raise
            
    def commandEDMdata(self, filenametxt, command: str):
        data_in_buffer =True
        ok_num =0
        opened_port =False
        # Open a serial Port
        com = serial.Serial()
        com.baudrate = 57600
        com.port = self.port
        #com.port = '/dev/ttyUSB0'
        com.exclusive = True
        com.timeout = 180
        com.xonxoff = True
        print(com.isOpen())
        if com.isOpen() is True:
            print("Serial port is in use not recording data")
            exit(-1)
        try:
            com.open()
        except Exception as e2:
            print("Failed to open Serial port \nCheck it is not opened elsewhere")
            print(str(e2))
            exit(-2)
        else:
            print("serial port opened")


        #open a text file to log data
        try:
            if filenametxt == 'create_new_text_test.txt':
                test = open(filenametxt, 'wb')
                test.close
                exit(1)
            txt = open(filenametxt,'wb')

        except Exception as e3:
            print(str(e3))
            exit(-2)
        try:
            #start timer to ensure the program doesn't get stuck
            tic=timeit.default_timer()
            print("writing to EDM: ", command)
            # clear the stack for the EDM
            send = ' ..\r'
            com.write(send.encode())
            # Send command to print logged data
            send = command + '\r'
            com.write(send.encode())
            # while there is data in the buffer echo it back to the terminal
            
            while data_in_buffer:
                data = com.read_until(b'\r\n')
                data = data.decode('ascii', 'ignore')
                data = data.replace('\x11','')        #Ignore unknown Ascii characters
                txt.write(data.encode('ascii'))
                if data.find('ok') == -1:
                    toc = timeit.default_timer();
                    if(toc-tic)>900:
                        data_in_buffer = False
                        print('Serial Port Timeout over 15 minutes to recieve all data')
                    pass
                else:
                    #time.sleep(2)
                    ok_num= ok_num+1
                    if ok_num ==2:
                        data_in_buffer =False
                        print('Buffer is empty\n')
            txt.close()
            com.close()
        except Exception as e1:
            print("error in comminucations \n" + str(e1))
            txt.close()
            com.close()
            raise


class TestreadEDM(unittest.TestCase):
    
    def setUp(self):
        self.EDM =EDMSerial()
    
    def test_wrong_port(self):
        with self.assertRaises(SystemExit) as output:
            self.EDM.getEDMdata('unitttest_wrongport.txt')
        self.assertEqual(output.exception.code,-2)
        
    # This will change depending on system, on RPi will get -2 on mac recives -1 expection
    def test_port_is_open(self):
        self.EDM.changePort('/dev/cu.usbserial-240')
        com = serial.Serial()
        com.baudrate = 57600
        com.port = self.EDM.port
        #com.port = '/dev/ttyUSB0'
        com.exclusive = True
        com.timeout = 180
        com.xonxoff = True
        com.open()
        self.EDM.changePort('/dev/cu.usbserial-240')
        with self.assertRaises(SystemExit) as output:
            self.EDM.getEDMdata('unitttest_openport.txt')
        self.assertEqual(output.exception.code,-2)
        com.close()
        
        
        
    def test_file_is_created(self):
        self.EDM.changePort('/dev/cu.usbserial-240')
        with self.assertRaises(SystemExit) as output:
            self.EDM.getEDMdata('create_new_text_test.txt')
            self.assertTrue(os.path.isfile('create_new_text_test.txt'))
        self.assertEqual(output.exception.code,1)
        os.remove('create_new_text_test.txt')
    
    def test_data_recieved(self):
        self.EDM.changePort('/dev/cu.usbserial-240')
        self.EDM.getEDMdata('size_test.txt')
        self.assertGreater(os.path.getsize('size_test.txt'),200000)
        os.remove('size_test.txt')
#unittest.main()


