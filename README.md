# Remote-PI-Logging
This repository contains the approprite python scripts to operate the the EDM's remotely using Raspberry Pi's 

For inforamtion regarding how to set up a fresh Rasperry Pi from a backup image (clean or used) please see the cloning instructions in the setup folder.

**When running any programs that communicate with the EDM (loggingGit.py, BOOTSTRAP.py) ensure that minicom is closed** to check if a minicom terminal is open run the following command

      ps aux | grep minicom

If you recive more than one output line (ie one other than the one from the grep command) there is a minicom terminal open. It can be killed using the folowing command

      sudo kill -9 <PID>

Where the PID is the number in the coloumn following pi.

## Cronjob Logging

The RPi is set up for scheduled running of the loggingGit.py script (information laid out below). This is done through the linux cron system, by defualt on a CLEAN image for the RPis this is disabled. To start automatic logging run the following command:

      conrtab -e 

This will open up the cron tab editor. The last line of this file is the section for running the cronjob it should look like this: _(this line may be incorrect in CLEAN installations)_.

      #0 * * * *  ./Remote-PI-Logging/loggingGit.py  >> test.out

By uncommenting this line and saving the file (**ctrl+x** then **y** then **enter**) the cronjob will run every hour. The logging and output information and any error messages can be found in **test.out**. This frequency can change by adjusting the '0 * * * *' at the start of the line. More information about how to adjust these values can be found [here](https://crontab.guru). It should be noted that it does take time for the EDM to print all of its data. should there be any serial issues (partial reads) the program will wait for 15min on the serial port before procceding. Please take this into account.

Ensure to disbale this functionality when using minicom for extened periods of time or when reprogramming the EDM. This can be done by editing the tab and commenting out the line.

## Available Programs 
There are currently 3 available programs to assist with logging data from the EDM, programming the EDM and cycling power to the EDM (if relays are connected)

Before running any of the programs ensure that they are up to date by running the bash script in the home directory of the Pi

      ./updatescripts.sh

This file is also located in this git repository should it not be in the pi home directory run this command instead

      chmod +x Remote-PI-Logging/updatescripts.sh
      ./Remote-PI-Logging/updatescripts.sh      

This will update the scripts on the pi and ensure they are executable. All instructions will be assuming you are running the programs from the home directory and as such running them from within the Remote-PI-Logging directory may effect functionality. 

### BOOTSRTRAP.py

This program is for re-programming the EDM from the RPi, it is called using the following structure

      ./Remote-PI-Logging/BOOTSTRAP.py <option> [hexfile]

Acceptable options are:

  <-h>            help, will explain options
  
  <-R>            Reset, will send a reset comannd to the EDM
  
  <-P> [hexfile]  Will program the EDM with the presented hexfile. Hexfile is required for programming.

### CycleEDM.py

This program will cycle the first Relay on the Relay hat. If this is connected to the EDM it will cycle the EDM power. It should be called in the following manner 

      ./Remote-PI-Logging/CycleEDM.py

### loggingGit.py

This is the automated logging script. It has several section each have been separated into several subs scripts which are called from this main program.
To manually run this program call the following command

      ./Remote-Pi-Logging/loggingGit.py

This will call do the following steps.

#### Reading from the EDM
The first section of the script opens a serial port to the EDM and requests that the EDM sends through its stored data in decimal form. This is then saved directly to a file in the **data_backup** directory. The naming scheme for these files is **yyyy_mm_dd__HH_MM.txt**. The rest of the program uses this file to asses the data and construct consequent files.

#### Assesing and Padding Raw Data
The following section filters through the raw data to assertain the time in seconds between each timestamped record in the data set and the number of data entries between each time stamp. It uses these 2 pieces of information to asses whether the data is missing any sections (non-continous time stamps) and will pad the missing section with 0s. It will also add approprite timestamps to match the raw data. **Should the sections be discontinous by more than a day (24hrs) the script will ignore the older data** assuming it to be not required (this data is still presever in the data_backup directory). Should the EDM print send a section of Erased memory (_identifiable by the uniquie timestamps_) this will be replaced and back padded with 0s to fill up the dataset. This padded datafile will be saved to the **data_pad** directory with the naming convention of **yyyy_mm_dd__HH_MMpad.txt**.

#### Appending to a Continous data set.
The final section of the program appeneds the newly recieved data to a .txt file to produce a continous data set. This is done by searching for the the last timesatmp in the continous set to see if it is present in the new data form the padded file. If so it is appened directly to the large dataset from the following timestamp. Should the timestamp not be found the diffrence between the closest time and the last time is assesed and if it is less that 24hrs the data will be padded with 0s and appeneded. If the time is greater that 24hrs it will be separated by a number of #s and added as a new section. This large data file is called **datatext.txt**.

### TO DO

File containing only timestamped data (Ross)

Addnig timestamps to all data points 

Graphana or other web server plotting 

Compression and data managment
- using numpy and scipy to store the concatenated data for MATLAB
- potentially making the storage of the padded files optional (ie removing them after appending)
