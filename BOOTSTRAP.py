#!/usr/bin/python2.7

# test script to call a terminal and read data from an EDM

import serial
import time
import sys
import getopt
import os
import subprocess
send = ''
hexfile =''
reset = False
def do_command():
    #set baudarte
    baud = 19200
    global send
    global hexfile
    global reset
    # Open a serial Port
    if reset:
        com = serial.Serial()
        com.baudrate = baud
        com.port = '/dev/ttyUSB0'
        com.exclusive = True
        if com.isOpen() is True:
            print("Serial port is in use not recording data")
            exit()
        try:
            com.open()
        except Exception, e2:
            print("Failed to open Serial port \nCheck it is not opened elsewhere")
            print(str(e2))
            exit("-1")
        else:
            print("serial port opened")

        try:
        
            # Send command
            #send = '\x01CSS0R'
            print(send)
            com.write(send.encode())
            com.close()
            sys.exit(1)
        except Exception, e1:
            print("error in comminucations \n" + str(e1))
            
    if os.path.exists(hexfile):
        pass # append if already exists
    else:
        print("Path to file does not exist: "+hexfile)
        sys.exit(2)
    com = serial.Serial()
    com.baudrate = baud
    com.port = '/dev/ttyUSB0'
    com.exclusive = True
    #print(com.isOpen())
    if com.isOpen() is True:
        print("Serial port is in use not recording data")
        exit()
    try:
        com.open()
    except Exception, e2:
        print("Failed to open Serial port \nCheck it is not opened elsewhere")
        print(str(e2))
        exit("-1")
    else:
        print("serial port opened")

    try:
        
        # Send command
        #send = '\x01CSS0R'
        print(send)
        com.write(send.encode())
        com.close()
        time.sleep(0.1)
        subprocess.call(["msp430-bsl","-evvv","--erase=0x1100/2","--debug","-S","-p","/dev/ttyUSB0",hexfile])
        #os.system("msp430-bsl -evvv --erase=0x1100/2 --debug -S -p /dev/ttyUSB0 "+hexfile)
    except Exception, e1:
        print("error in comminucations \n" + str(e1))

def main(argv):
    global send
    global hexfile
    global reset
    try:
        opts, args = getopt.getopt(argv,"hPR")
    except getopt.GetoptError:
        print("BOOTSTRAP.py\n-R for reset\n-P <hexfile> to program hexfile to the EDM")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("BOOTSTRAP.py\n-R for reset\n-P <hexfile> to program hexfile to the EDM")
            sys.exit()
        elif opt == "-R":
            send ='\x01CSS0R\n\r'
            print("writing Reset command to Bootloader: ctrl-aCSS0R")
            reset = True
        elif opt in "-P":
            send ='\x01CSS0P\n\r'
            hexfile = args[0]
            print("writing Program command to Bootloader: ctrl-aCSS0P")
            print("Proggraming "+hexfile)
if __name__ == "__main__":
    main(sys.argv[1:])
    do_command()
