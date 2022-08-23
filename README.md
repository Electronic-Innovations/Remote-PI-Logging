# Remote-PI-Logging
This repository contains the approprite python scripts to operate the the EDM's remotely using Raspberry Pi's 

For inforamtion regarding how to set up a fresh Rasperry Pi from a backup image (clean or used) please see the cloning instructions in the setup folder.

## Available Programs 
There are currently 3 available programs to assist with logging data from the EDM, programming the EDM and cycling power to the EDM (if relays are connected)

Before running any of the programs ensure that they are up to date by running the bash script in the home directory of the Pi

      ./updatescripts.sh

This will update the scripts on the pi and ensure they are executable. All instructions will be assuming you are running the programs from the home directory and as such running them from within the Remote-PI-Logging directory may effect functionality.

### BOOTSRTRAP.py

This program is for re-programming the EDM from the RPi, it is called using the following structure

      ./Remote-PI-Logging/BOOTSTRAP.py <option> [hexfile]

Acceptable options are
  <-h>            help, will explain options
  <-R>            Reset, will sent a reset comannd to the EDM 
  <-P> [hexfile]  Will program the EDM with the presented hexfile. Hexfile is required for programming.

### CycleEDM.py

This program will cycle the first Relay on the Relay hat. If this is connected to the EDM it cycle the EDM power. It should be called in the following manner 

      ./Remote-PI-Logging/CycleEDM.py

### loggingGit.py

This is the automated logging script. It has several section each have been separated into several subs scripts which are called from this main program.

#### Reading from the EDM
The first section of the script opens a serial port to the EDM and requests that the EDM sends through its stored data in decimal form. This is then saved directly to a file in the *data_backup* directory. The naming scheme for these files is *yyyy_mm_dd__HH__MM.txt*. The rest of the program uses this file to asses the data and construct consequent files.

#### Assesing and Padding Raw Data
The following section filters through the raw data to assertain the time in seconds between each timestamped record in the data set and the number of data entries between each time stamp. It uses these 2 pieces of information to asses whether the data is missing any sections (non-continous time stamps) and will pad the missing section with 0s. It will also add approprite timestamps to match the raw data. *Should the sections be discontinous by more than a day (24hrs) the script will ignore the older data* assuming it to be not required (this data is still presever in the data_backup directory). Should the EDM print send a section of Erased memory (_identifiable by the uniquie timestamps_) this will be replaced and back padded with 0s to fill up the dataset.
