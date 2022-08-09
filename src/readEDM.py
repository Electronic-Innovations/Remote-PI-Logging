'''
Module for probing the EDM to output all of its memory and directly copy this output to the provided text file
Defaults to port '/dev/ttyUSB0'
'''


import serial
import timeit
import os


def getEDMdata(filenametxt,port='/dev/ttyUSB0'):
    data_in_buffer =True
    ok_num =0
    # Open a serial Port
    com = serial.Serial()
    com.baudrate = 57600
    com.port = port
    #com.port = '/dev/ttyUSB0'
    com.exclusive = True
    com.timeout = 180
    com.xonxoff = True
    print(com.isOpen())
    if com.isOpen() is True:
        print("Serial port is in use not recording data")
        exit()
    try:
        com.open()
    except Exception as e2:
        print("Failed to open Serial port \nCheck it is not opened elsewhere")
        print(str(e2))
        exit("-1")
    else:
        print("serial port opened")


    #open a text file to log data
    try:
        txt = open(filenametxt,'wb')

    except Exception as e3:
        print(str(e3))
        
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
