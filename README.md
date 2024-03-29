# Remote-PI-Logging
This repository contains the appropriate python scripts to operate the the EDM's remotely using Raspberry Pi's 

For information regarding how to set up a fresh Raspberry Pi from a backup image (clean or used) please see the cloning instructions in the setup folder.

**When running any programs that communicate with the EDM (loggingGit.py, BOOTSTRAP.py) ensure that minicom is closed** to check if a minicom terminal is open run the following command

      ps aux | grep minicom

If you receive more than one output line (i.e., one other than the one from the grep command) there is a minicom terminal open. It can be killed using the following command

      sudo kill -9 <PID>

Where the PID is the number in the column following pi.

Most RPis will be equiped with a cron job that will automatically kill any minicom terminal on the 55th minute of the hour.

      55 * * * * pkill minicom
      
For more information about cronjobs see the following section.

## Cronjob Logging

The RPi is set up for scheduled running of the loggingGit.py script (information laid out below). This is done through the linux cron system, by default on a CLEAN image for the RPis this is disabled. To start automatic logging run the following command:

      conrtab -e 

This will open up the cron tab editor. The last line of this file is the section for running the cronjob it should look like this: _(this line may be incorrect in CLEAN installations)_.

      #0 * * * *  /home/pi/Remote-PI-Logging/loggingGit.py  >> test.out

By uncommenting this line and saving the file (**ctrl+x** then **y** then **enter**) the cronjob will run every hour. The logging and output information and any error messages can be found in **test.out**. This frequency can change by adjusting the '0 * * * *' at the start of the line. More information about how to adjust these values can be found at [Crontab Guru](https://crontab.guru). It should be noted that it does take time for the EDM to print all of its data. should there be any serial issues (partial reads) the program will wait for 15min on the serial port before proceeding. Please take this into account.

Ensure to disable this functionality when using minicom for extended periods of time or when reprogramming the EDM. This can be done by editing the tab and commenting out the line.

An example of the crontab entries are shown below.

	0 * * * *  /home/pi/Remote-PI-Logging/loggingGit.py  >> test.out
	55 * * * * pkill minicom
	30 12 * * *  /home/pi/Remote-PI-Logging/Cleanup.py  >> removed.out
	20-50 0-23/1 * * * /home/pi/Remote-PI-Logging/loggingJGRAB.py >> testJGRAB.out

## Available Programs 
There are currently 4 available programs to assist with logging data from the EDM, programming the EDM and cycling power to the EDM (if relays are connected)

Before running any of the programs ensure that they are up to date by running the bash script in the home directory of the Pi

      ./updatescripts.sh

This file is also located in this git repository should it not be in the pi home directory run this command instead

      chmod +x Remote-PI-Logging/updatescripts.sh
      ./Remote-PI-Logging/updatescripts.sh      

This will update the scripts on the pi and ensure they are executable. All instructions will be assuming you are running the programs from the home directory and as such running them from within the Remote-PI-Logging directory may affect functionality. 

### BOOTSTRAP.py

This program is for re-programming the EDM from the RPi, it is called using the following structure

      ./Remote-PI-Logging/BOOTSTRAP.py <option> [hexfile]

Acceptable options are:

  <-h>            help, will explain options
  
  <-R>            Reset, will send a reset command to the EDM
  
  <-P> [hexfile]  Will program the EDM with the presented hexfile. Hexfile is required for programming.

### CycleEDM.py

This program will cycle the first Relay on the Relay hat. If this is connected to the EDM it will cycle the EDM power. It should be called in the following manner 

      ./Remote-PI-Logging/CycleEDM.py

### Cleanup.py

This program removes older logged data from the **data_backup** and **data_pad** directories. It is to be setup in the form of a cronjob and will only removed files should the RPi have less than 2GB of storage remaining. It will removed the oldest log files indicated by the filename progressively until 2GB of space is freed. This script can also be called manually by:

    ./Remote-PI-Logging/Cleanup.py

The cronjob for this task will need to be implemented on a case-by-case basis however a check once a day should be sufficient to ensure that that RPi does not fill up its storage in most cases. The following line will need to be added to the Cron tab for this cleanup function to work.

          30 12 * * *  ./Remote-PI-Logging/Cleanup.py  >> removed.out

This will perform a check at 12:30pm everyday to ensure the memory has more than 2Gb of space. See the Cronjob logging section for more information about the crontab.
It should be noted that **datatext.txt** and **test.out** are not removed by this script and continue to grow, these will need to be removed manually by a user using the following commands from the home directory 

      rm test.out
      rm datatext.txt
      touch test.out
      touch datatext.txt
      
This will remove them and create empty files in their place.

### loggingGit.py

This is the automated logging script. It has several sections, each have been separated into several subs scripts which are called from this main program.
To manually run this program call the following command

      ./Remote-Pi-Logging/loggingGit.py

This call will do the following steps.

#### Reading from the EDM
The first section of the script opens a serial port to the EDM and requests that the EDM sends through its stored data in decimal form. This is then saved directly to a file in the **data_backup** directory. The naming scheme for these files is **yyyy_mm_dd__HH_MM.txt**. The rest of the program uses this file to asses the data and construct consequent files.

#### Assessing and Padding Raw Data - Not Required if graphing with Graph.py and _graph.py
The following section filters through the raw data to ascertain the time in seconds between each timestamped record in the data set and the number of data entries between each time stamp. It uses these 2 pieces of information to asses whether the data is missing any sections (non-continuous time stamps) and will pad the missing section with 0s. It will also add appropriate timestamps to match the raw data. **Should the sections be discontinuous by more than a day (24hrs) the script will ignore the older data** assuming it to be not required (this data is still preserved in the data_backup directory). Should the EDM print send a section of Erased memory (_identifiable by the unique timestamps_) this will be replaced and back padded with 0s to fill up the dataset. This padded datafile will be saved to the **data_pad** directory with the naming convention of **yyyy_mm_dd__HH_MMpad.txt**.

#### Appending to a Continuous data set - Not Required if graphing with Graph.py and _graph.py
The final section of the program appends the newly received data to a .txt file to produce a continuous data set. This is done by searching for the last timestamp in the continuous set to see if it is present in the new data form the padded file. If so it is appended directly to the large dataset from the following timestamp. Should the timestamp not be found the difference between the closest time and the last time is assessed and if it is less that 24hrs the data will be padded with 0s and appended. If the time is greater than 24hrs it will be separated by a number of #s and added as a new section. This large data file is called **datatext.txt**.


# Graphing and Data Processing
A python based graphing and processing utility has been added which utilises Pandas, Numpy and Matplotlib. These packages will need to be installed on any device which wishes to utilise this module. It is not advised to use the RPIs for this process and it should be completed on an office computer or laptop. This module also allows the user to convert the text files of data to compressed csv files, join several text files together and complete basic data scaling. The main module of this utility can be found at **graph_src/Graph.py** and contains detailed descriptions of how the module operates and available functions. A test script showing the usage in python of this module can be found at **graph_src/_graph.py**.

To use this module for an explicit data set ensure that Pandas, Numpy and Matplotlib are installed by running the following commands:

      pip3 install pandas
      
      pip3 install numpy
      
      pip3 install matplotlib

This can be done in the standard or a virtual environment. Copy **Graph.py** and **_graph.py** to the same directory as your datafile/s Then modify **_graph.py** with the appropriate settings selected (OpenCsv, single_file, channel_names etc). To run the script navigate to the directory of the script in a terminal and run:

      python3 _graph.py
      
Ensure that the file name or directory for the data in _graph.py is correct. Furthermore several pieces of information from the data file are required by the user in _graph.py (hexadecimal, instantaneous data, Csv file, saving etc) and these need to be selected appropriately. For example if you do not select __ints_data__ but select Graph_ints and/or Graph_2y_ints these plots will be ignored.

Finally if processing multiple data files it is recommended to do preliminary plotting to ensure the data is converted appropriately and save it as a compressed csv by setting:

      save = True

As this will significantly reduce the subsequent processing time for creating specific and more precise plots as the data will have to be processed every time. It is much quicker just to load in a csv.zip 
### TO DO

Reassess the padding functionality of loggingGit.py as the graphing utility does not require it and it may be redundant. (currently completely not utilised by the python graphing utility)

File containing only timestamped data (Ross) - can plot exclusively stamped data (Can be done using the graphing utility)

Adding timestamps to all data points - done in the graphing utility 

Graphana or other web server plotting 

Compression and data management - graphing utility saves data to a compressed csv
- using numpy and scipy to store the concatenated data for MATLAB
- potentially making the storage of the padded files optional (ie removing them after appending)

git clone https://github.com/Electronic-Innovations/Remote-PI-Logging.git
