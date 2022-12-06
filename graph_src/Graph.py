#!/graph_env/bin/python3
'''
Main Module
This program has been developed to read in an EDM datafile (.txt extention or .dta) and convert
    it to a pandas dataframe using the method mkdata().

    Lines starting with '', '%', '%%%','ok' or 'SSPRD_ALL' will be skipped. End line comments should be marked as '%%'. A single '%' in line markes an EDM datestamp
    
    This data frame can be saved as a compressed csv file
    with either 'zip' or 'gzip' compresssion using the method save_compress().
    
    Can add a full collumn of timestamps,
    completed by ext_time_d() and is required if plotting all the data and recomened before saving.
    
    Method name_channel() provides options to name the data channels and will appear as a legend.

    Dependencies:
        Numpy
        Pandas
        Matplotlib

    Main Methods:
        Graphing(filename, hexflag=False)

            Class constructor creates an instance of the Gaphing class.

            Inputs:
                filename - data file to read
                hexflag - a True/False flag to let the program know if the data is in hexadecimal
            
    
         mkdata(width = None, width_t = None, depth = None )

             Method which uses the filename in the constructed class to search the current directory for the file
             then brings it into the program as a pandas dataframe. Input variables are used following a histogram of the data.
             Using these variables will select the width of the data and should be found as the bins with largest two counts
             from the histogram functions. width_t = width +1 as per how mkdata runs. Depth is provided from histogram_data() and is the number of
             rows between timestamps.
             All inuput variables are required when data filtering. Filtering occurs by checking of each row matches eitehr width or width_t
             if not the entire stamped section is removed, simmiarly if the rows do not match that stamped section will be removed.

             Features:
                 Reads each line indifidually and breaks them up on whitespace. Searches for '%' to mark date stamps
                 Records the number of columns in reach row
                 Records the number of rows between timestamps

            Inputs:
                width - the bin with the largest count from histogram_data()
                width_t - the bin with the second largest count form histogram_data() (width_t = width + 1)

            Dependencies:
                Graphing()


        ext_time_d()

            Method which exteds the time stamps in a the 'Time' column to mark every data item.

            Features:
                Dynamicaly assesses the difference between each row by using the difference between each time step and  number of rows between them
                Uses local information (current stamp, past stamp and future stamp)

            Dependencies:
                Graphing()
                    mkdata() or open_csv()


        name_channel(namelist)

            Method for renaming the columns of a data frame. Will also change the legend and other labelling info

            Inputs:
                namelist - a list of strings corresponding to columns of data the data frame

            Dependencies:
                Graphing()
                    mkdata() or open_csv()
                    

        mkGraph_add(specific =None, start_time = None)

            Method for plotting a single graph containing all rows from the dataframe

            Inputs:
                specific - A list of column titles as strings to plot. Selects these columns and only plot them together.
                start_time - A time string for selecting the time where to start plotting (can cause issues if the data set has double ups of the closest time after the selected one)
                             String format "YYYY-MM-DD HH:MM:SS"

            Dependencies:
                Graphing()
                    mkdata()
                        ext_time_d()
                        

        mkGraph_all_add(start_time = None)

            Method for plotting all the data rows againts the created time stamps with each channel on a its own plot.

            Inputs:
                start_time - A time string for selecting the time where to start plotting (can cause issues if the data set has double ups of the closest time after the selected one)
                             String format "YYYY-MM-DD HH:MM:SS"

            Dependencies:
                Graphing()
                    mkdata()
                        ext_time_d()


        mkGraph_true(specific = None, start_time = None)            

            Method for plotting a single graph containing all columns and only the EDM timestamped data rows

            Inputs:
                specific - A list of column titles as strings to plot. Selects these columns and only plot them together.
                start_time - A time string for selecting the time where to start plotting (can cause issues if the data set has double ups of the closest time after the selected one)
                             String format "YYYY-MM-DD HH:MM:SS"

            Dependencies:
                Graphing()
                    mkdata()

                        

        mkGraph_all_true(start_time = None)

            Same as mkGraph_true but each columns has its own plot.

            Inputs:
                start_time - A time string for selecting the time where to start plotting (can cause issues if the data set has double ups of the closest time after the selected one)
                             String format "YYYY-MM-DD HH:MM:SS"

            Dependencies:
                Graphing()
                    mkdata()


        mkGraph_ints()

            Specific plotting fucntion to plot instantaneous data.

            Features:
                Does not plot against time just plots data sequentially

            Dependencies:
                Graphing()
                    mkdata()


        save_compress(flag)

            Method for saving the dataframe in its current state to a compressed .csv file

            Inputs:
                flag - slected compression type 'zip' or 'gzip'

            Outputs:
                Compressed file with the name "'filename'New.csv.zip" or "'filename'New.csv.gz"

            Dependencies:
                Graphing()
                    mkdata() - required
                        ext_time_d() -recomended
                            Convert_channel() - recomended
                            

        join_data_text(filelist,outfile)

            Method that produces a single datafram by creating and joining data frames made form all the files listed in filelist.
            This is completed by running mkdata with each file sequetially and joining the resulting data frames.

            Inputs:
                filelist - a list of strings which are files in the local directory
                outfile -  a string which is the designated name for a file created from

            Dependencies:
                Graphing()


        open_csv(filename)

            Method for retriveing a dataframe saved as a compressed csv by the save_compress method

            Inputs:
                filename -  a string which is the filename of a compressed csv file created by save_compress()

            Dependencies
                Graphing()
                

        Convert_channel(channel, scale_factor)

            Method which will scale the data igiven  factor which represents the unit per division in the the data set.

            Inputs:
                channel - string for the column name to convert
                scale_factor - int representing the number that the mean of the data is

            Dependecies:
                Graphing()
                    mkdata()

            Notes
                    - needs to be made with more depth, would like to be able to scale with what one value is equal to.


        Subplot_data(columns, method = 'Time_real', fontsize = 18,legendsize = 10, yaxis = 'yaxis', xaxis = 'Date and Time', ylabels = None, ylim = None))

            Method to create a figure with subplots for specific columns of data.

            Inputs:
                columns - a list of strings containing the columns that need to be plotted. Also accepts a list of lists where each list is a list of strings to plot multiple lines per subplot
                method - a string selector
                        'Time_real' - will only plot time stamps from the EDM
                        'Time_all' - will plot all rows of data with generated time stamps
                fontsize - an int relating to the fontsize of the major axis labels
                legendsize - an int relating to the size of the plot legends
                yaxis - a string to print as the major y-axis label
                xaxis - a string to print as the major x-axis label
                ylabels - a list represending the minior y-axis labels
                ylim - a list of list containing the y axis limits for each subplot
                        [[None,None], [10,111], [-3,15]] would use auto limits for the first plot then the defined limts for the following plots

            Dependencies:
                Graphing()
                    mkadata()
                        ext_time_d() - 'Time_all' option only


        Remove_None()

            Method for removing section of the data file that have a reduced number of columns. Does not
            work for datasets with sections that have an increased number of columns. Needed for plotting if data is funky.

            Dependencies:
                Graphing()
                    mkdata()


        Histogram_data()

            Method that uses information gathered in mkdata() about the width of the EDM pages and the depth of the EDM pages
            to produce a histogram of the number of columns read into the data frame should produce 2 bis of data (timestamped and non-timestamped sections).
            It will also create a histogram of the number of rows between time stamps (EDM page size).

            Dependencies:
                Graphing()
                    mkdata()


        collect_files(directory = "", extension = ".txt")

            Method used to collect all the files in a give directory with a given extention. this list can be provided to join_data_text()
            it y default searches the current directory and for .txt files.

            Inputs
                directory - the directory to search (relative or root path)
                extension - the file extension to search for (defaults to .txt)


        single_plot_2y(axis1, axis2, colours, method = 'Time_real', xaxis = "time", yaxis ="data",yaxis2 = "data2", legendsize = 10)

            Method used to plot several columns of data on a single plot with 2 separate y-axis              

            Inputs:
                axis1 - a list of strings containing the columns that need to be plotted on the left y-axis
                axis2 - a list of strings containing the columns for the right y-axis
                colours - a list of colours to plot the lines in. Required to have enough for eaxh line to be plotted.
                method - a string selector
                        'Time_real' - will only plot time stamps from the EDM
                        'Time_all' - will plot all rows of data with generated time stamps
                legendsize - an int relating to the size of the plot legends
                yaxis - a string to print as the left y-axis label
                yaxis2 - a string to print as the right y-axis label 
                xaxis - a string to print as the major x-axis label

            Dependencies:
                Graphing()
                    mkadata()
                        ext_time_d() - 'Time_all' option only

        single_plot_2y_ints(axis1, axis2, colours, method = 'Time_real', xaxis = "time", yaxis ="data",yaxis2 = "data2", y2lim = None, legendsize = 10,samplecut = 0,samplefact = None)

            Method used to plot several columns of data on a single plot with 2 separate y-axis for instantaneous data               

            Inputs:
                axis1 - a list of strings containing the columns that need to be plotted on the left y-axis
                axis2 - a list of strings containing the columns for the right y-axis
                colours - a list of colours to plot the lines in. Required to have enough for eaxh line to be plotted.
                method - a string selector
                        'Time_real' - will only plot time stamps from the EDM
                        'Time_all' - will plot all rows of data with generated time stamps
                legendsize - an int relating to the size of the plot legends
                yaxis - a string to print as the left y-axis label
                yaxis2 - a string to print as the right y-axis label 
                xaxis - a string to print as the major x-axis label
                y2lim - a list defining the second y-axis limits
                samplecut - number of data points to skip into the data
                samplefact - a scaling factor for the x-axis to convert samples to time.

            Dependencies:
                Graphing()
                    mkadata()
                        ext_time_d() - 'Time_all' option only
                        
    
'''

import glob
import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


class Graphing:

    # Basic Inilisation for the class (most info comes from the mkdata() method)
    def __init__(self,filename, hexflag = False):
        self.filename=filename
        self.dataframe = []
        self.pdData = None
        self.hexflag = hexflag
        self.convert_flag = False
        self.histogram_arr_width = []
        self.histogram_arr_depth = []

    # DEPRECIATED - Use ext_time_d() for dynamic time extention
    # Method to fill the 'Times' coloumn with data. Takes the time step and sequentially adds
    #   one step per line of data starting from each line already with a timestamp
    def extendtime(self):
        size = self.pdData.shape[0]
        for i in range(size):

            # If time value is NA
            # value = (prev timestamp) + (time_step)*(rows since prev timestamp)
            if pd.isna(self.pdData.loc[i,'Time']):
                self.pdData.loc[i,'Time'] = temp + pd.to_timedelta(count, unit ='s')
                count +=self.time_step
                
            # Otherwise use the real timestamp
            else:
                count = 0
                temp = self.pdData.loc[i,'Time']
                count +=self.time_step
            

    # Method to adaptively fill the 'Time' coloumn with timestamps. Uses the surrounding timestamps
    # and number of data points between them to determine the timezone of the data and label it
    def ext_time_d(self):
        col = self.pdData.loc[:,'Time']
        col = col.notna().to_numpy()
        idx = np.where(col == True)
        idx = list(idx[0])                                                                              #Collect row indexs for each timestamp in the data frame
        for i in range(len(idx)):
            if i == 0: continue                                                                         # Loop over indexs (skip the first one so we can compare backwards)
            if i == 1: old_diff = self.pdData.loc[idx[i],'Time'] - self.pdData.loc[idx[i-1],'Time']     # For the first section set old_diff the same as the current one
            steps= idx[i]-idx[i-1]                                                                      # calaculate data points between time current and prev time
            time_diff = self.pdData.loc[idx[i],'Time'] - self.pdData.loc[idx[i-1],'Time']               # calculate current time difference
            if old_diff != time_diff:                                                                   # compare current time difference to previous time difference (if not the same handle)
                try: # Section for handling discontinuity and timezone shifts
                    future_diff = self.pdData.loc[idx[i+1],'Time'] - self.pdData.loc[idx[i],'Time']     #calaculate the next zones time diff
                    if time_diff == future_diff:                                                        # If current and futuer time_diff is the same trust the calculated timedelt
                        timedelt = time_diff/steps
                    else:                                                                               # if Current time_dif is not the same as the future diff or
                        timedelt = timedelt                                                             # the past diff then do not change timedelt (trust that the timing is the same as pervious)
                except Exception as e1:                                                                 # handle excption for discontiuity at the end of data, (use previous timedelt not enough info to 100%)
                    print(e1)
                    print("incontinuity in last section page of data using previous timedelta")
                    timedelt =timedelt
            else:                                                                                       # If no incontinuity use caculated timedelt
                timedelt =  time_diff/steps
            for k in range(steps):
                if k == 0: continue
                self.pdData.loc[idx[i-1]+k,'Time'] = self.pdData.loc[idx[i-1]+k-1,'Time'] + timedelt    # Apply timedet incrementaly to each data point between indexes (skip fist as its already got a time)
            old_diff = time_diff
        for k in range(steps):
            if k == 0: continue
            self.pdData.loc[idx[-1]+k,'Time'] = self.pdData.loc[idx[-1]+k-1,'Time'] + timedelt          # After looping use last timedelt to label the last page of data
        #print(self.pdData.loc[:,'Time'].to_string())
        #print(self.pdData.to_string())
        
    # Method that creates a pandas dataframe from a text file.        
    def mkdata(self, width = None, width_t = None, depth = None):

        #Open file
        with open(self.filename,'r') as datafile:
            lines = datafile.readlines()        # Read in lines
            started = False                     # Start copying flag is false
            time = False                        # Time stamp Flag is false
            comment = False                     # Comment Flag is false
            pop = False
            row_num = 0                                    # Flags are used during the read
                                                #   process to keep column number conistent.
            vect = []                           # Empty list for appending
            timedata=[]                         # Special Timedata variable

            #Cycle through each line of file
            for line in lines:
                line = ''.join([x for x in line if x in string.printable])  # check for non-printable charachters and remove them
                
                if line.upper().isupper() and self.hexflag == False and (line.find('ok') == -1):      #If the line contains any letters (non-hex data) and skip if so    
                    continue
                if line.find('%') !=-1:             # If has a % set start flag
                    if line.find('31:63:63') != -1: # If has erased time skip
                        continue
                    started =True               #   (first line should be a comment or have a timestamp with %)
                if started ==True:
                    linedata = line.split()

                    #Split line on whitespace and check if first elemet for (nothing, empty '', comment or split)
                    if not linedata or linedata[0] == '' or linedata[0] == '%' or linedata[0] == '%%%' or linedata[0] == 'ok' or linedata[0] =='SSPRD_ALL' or linedata[0] =='..' or linedata[0] =='<sp' or linedata[0] =='d':
                        continue                # skip to next line if so

                    # Cycle each part of the line
                    for i in range(len(linedata)):
                        linedata[i] = linedata[i].replace('/x11','')
                        if linedata[i] == '%':  # Single % indicates timestamp
                            time = True         # Set flag, mark index and set timedata string move to next item
                            pos = i
                            timedata = ''
                            if depth is not None:
                                if (depth != row_num and row_num != 0) or pop:
                                    print("Bad data page found removing:")
                                    for p in range(row_num):
                                        temp = self.dataframe.pop()
                                        print(temp)
                                    row_num = 0
                                    pop = False
                                    
                                else:
                                    self.histogram_arr_depth.append(row_num)
                                    row_num =0
                            
                            continue
                        if linedata[i] == '%%': # Double % indicates comment set flag and break loop.
                            comment = True
                            break
                        if time == True:        # If time flag is set collect rest of line as one item
                            timedata += (' ') +linedata[i]


                    if time == True:            # If time flag is true vect is each element till pos plus timestamp
                        vect =(linedata[0:(pos)])
                        vect.append(timedata)
                        self.histogram_arr_width.append(len(vect))
                    elif comment:               # If comment flag is set vect is up until the latest i
                        vect = linedata[0:i]
                        self.histogram_arr_width.append(len(vect))
                    else:                       # Otherwise vect is every element
                        vect = linedata[0:i+1]
                        self.histogram_arr_width.append(len(vect))

                        # Remove any 'ok'
                        if not vect or (vect[len(vect)-1].find('ok') != -1):
                            vect = vect[0:len(vect)-1]
                        vect.append('')

                    #Useful Debug for finding areas of data that arent uniform in the file.
                    #print(vect)
                    #if(len(vect)> 10):
                        #raise Exception("stop")
                    self.dataframe.append(vect)     # append vect to a list of lists to make a dataframe
                    row_num = row_num+1
                        
                    if width is not None:
                        if len(vect) == width or len(vect) == width_t:
                            pass
                            
                        else:
                            pop = True                          # if width is defined but does not match do not include
                    else:
                        self.dataframe.append(vect)     # append vect to a list of lists to make a dataframe
                        row_num = row_num+1
                        
                       
                        
                    time =False                         # reset flags
                    comment = False
                    vect = []                           # empty variables
                    timedata =[]
                    
        
        self.pdData = pd.DataFrame(self.dataframe)                                                                                  # Create dataframe from list of lists
        temp = self.pdData.shape                                                                                                    # get axis length
        self.pdData["Time"] = pd.to_datetime(self.pdData[temp[1]-1],format=' %Y-%m-%d %H:%M:%S', errors = 'coerce')                 # Convert Time stamp strings to datetime objects
        self.pdData.rename(columns={(self.pdData.shape[1]-2):'Time_r'}, inplace = True)                                             # rename real stamp coloumn 'Time_r'
        self.pdData["Time_r"] = self.pdData["Time"]                                                                                 # Create new coloumn to be filled with created date time stamps
        self.columnNames = list(self.pdData.columns.values)                                                                         # Save the column names to the object for access later
        self.dataframe = []
        print(self.pdData)                                                                                                          # print dataframe to terminal

    # Method to name the data channels of the dataframe
    def name_channel(self,nameslist):
        num_names = len(nameslist)
        if num_names > (self.pdData.shape[1]-2):                                           # If too many names are given prompt the user and continue
            print("Too manny names")
            print("Ignoring")
            print(nameslist[(self.pdData.shape[1]-2):])
            temp = list(self.pdData.columns.values)                                         # Save the current names
            temp[:(self.pdData.shape[1]-2)] = nameslist[:(self.pdData.shape[1]-2)]          # replace current with the provided ones excluding 'Time' and 'Time_r' 
            self.pdData.set_axis(temp, axis =1, inplace= True)                              # apply to dataframe
            self.columnNames = list(self.pdData.columns.values)                             # Save new names to object
        else:
            temp =list(self.pdData.columns.values)                                          # If less than enough names replace those provided in order
            temp[:num_names] =nameslist
            self.pdData.set_axis(temp, axis =1, inplace= True)
            self.columnNames = list(self.pdData.columns.values)
        #print(self.pdData.to_string())
        print(self.columnNames)

    # Method for plotting all data with construced date time stamps
    def mkGraph_add(self, specific =None, start_time = None):
        #plt.figure()
        plot_data = self.pdData.sort_values(['Time'])
        plot_data = plot_data.set_index('Time')                       # Create temp data frame and set index to contructed date time stamps
        plot_data = plot_data.drop(columns='Time_r')                    # Drop real date time stamps from the set
        
        if start_time is not None:                                      # Check for ttime to start plotting
            times = plot_data.index.tolist()
            start = min(dt for dt in times if dt > (datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')))            # find earliest time after the input time
            
            plot_data = plot_data.loc[start:]                           # Adjust the plotting dataframe
        
        plot_data = plot_data.astype(str)                               # convert data to string type so it can be converted
        if self.hexflag:                                                # if file wad pased with hexflag convert coulmn data using int(data, base=16)
            for i in range(plot_data.shape[1]):
                plot_data[self.columnNames[i]] =plot_data[self.columnNames[i]].apply(int,base=16)
                
        else:                                                               # if no hex flag check if the data has been converted and set as float, if not set as int
            if self.convert_flag:
                plot_data = plot_data.astype(float)
            else:
                plot_data = plot_data.astype(int)
        print(plot_data)                                                    # print data frame to be plotted
        #plt.figure('All data')
        if specific == None:                                                # check if only specifc columns are to be plotted
            plot_data.plot(style = "-o", markersize= 1, linewidth = 0.5)    # plot dataframe with dots as data points and lines connecting them
        else:
            plot_data[specific].plot(style = "-o", markersize= 1, linewidth = 0.5) # plot data by indetifed columns names from 'specific' variable
        plt.legend(loc='upper right')
        
    # Method for plotting each data channel individually (all data)
    def mkGraph_all_add(self, start_time = None):
        plot_data = self.pdData.sort_values(['Time'])
        plot_data = plot_data.set_index('Time')                       # Create temp data frame and set index to contructed date time stamps
        plot_data = plot_data.drop(columns='Time_r')                    # Drop real date time stamps from the set

        if start_time is not None:                                      # Check for ttime to start plotting
            times = plot_data.index.tolist()
            start = min(dt for dt in times if dt > (datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')))            # find earliest time after the input time
            
            plot_data = plot_data.loc[start:]                           # Adjust the plotting dataframe
            
        plot_data = plot_data.astype(str)                               # convert data to integter type
        if self.hexflag:                                                # if file wad pased with hexflag convert coulmn data using int(data, base=16)
            for i in range(plot_data.shape[1]):
                plot_data[self.columnNames[i]] =plot_data[self.columnNames[i]].apply(int,base=16)
                
        else:                                                           # if no hex flag check if the data has been converted and set as float, if not set as int
            if self.convert_flag:
                plot_data = plot_data.astype(float)
            else:
                plot_data = plot_data.astype(int)
        print(plot_data)                                                # print data frame to be plotted
        for i in range(plot_data.shape[1]):                             # loop over data fram and plot each column on its own plot
            plt.figure(str(self.columnNames[i]))
            plot_data.loc[:,self.columnNames[i]].plot(style = "-o", markersize= 1, linewidth = 0.5)    # plot each column of the dataframe with dots as data points and lines connecting them
            plt.legend(loc='upper right')
    # Method for plotting only EDM timestamped data
    def mkGraph_true(self, specific = None, start_time = None):
        #plt.figure()
        plot_data = self.pdData                                         # Create temp dataframe
        plot_data = plot_data.drop(columns='Time')                      # Drop crontructed date time column 
        plot_data = plot_data[plot_data.Time_r.notnull()]               # remove rows with null date time stamps
        plot_data = plot_data.sort_values(['Time_r'])
        plot_data = plot_data.set_index('Time_r')                       # set index as date time stamps
        if start_time is not None:                                      # Check for ttime to start plotting
            times = plot_data.index.tolist()
            start = min(dt for dt in times if dt > (datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')))            # find earliest time after the input time
            plot_data = plot_data.loc[start:]                           # Adjust the plotting dataframe
            
        plot_data = plot_data.astype(str)                               # convert data to string tyoe type
        if self.hexflag:                                                # check hexflag and convert data if required
            for i in range(plot_data.shape[1]):
                plot_data[self.columnNames[i]] =plot_data[self.columnNames[i]].apply(int,base=16)
                
        else:                                                           # if no hex flag check if the data has been converted and set as float, if not set as int
            if self.convert_flag:
                plot_data = plot_data.astype(float)
            else:
                plot_data = plot_data.astype(int)
        print(plot_data)                                                # print data frame to be plotted
        if specific == None:
            plot_data.plot(style = "-o", markersize= 1, linewidth = 0.5)    # plot dataframe with dots as data points and lines connecting them
        else:
            plot_data[specific].plot(style = "-o", markersize= 1, linewidth = 0.5) #plot only specified columns with dots as data points and lines connecting them
        plt.legend(loc='upper right')
        
    # Method for plotting only EDM timestamped data individual columns
    def mkGraph_all_true(self, start_time = None):
        plot_data = self.pdData                                         # Create temp dataframe
        plot_data = plot_data.drop(columns='Time')                      # Drop crontructed date time column 
        plot_data = plot_data[plot_data.Time_r.notnull()]               # remove rows with null date time stamps
        plot_data = plot_data.sort_values(['Time_r'])
        plot_data = plot_data.set_index('Time_r')                       # set index as date time stamps

        if start_time is not None:                                      # Check for ttime to start plotting
            times = plot_data.index.tolist()
            start = min(dt for dt in times if dt > (datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')))            # find earliest time after the input time
            
            plot_data = plot_data.loc[start:]                           # Adjust the plotting dataframe
            
        plot_data = plot_data.astype(str)                               # convert data to string type
        if self.hexflag:                                                # check hexflag and convert data if required
            for i in range(plot_data.shape[1]):
                plot_data[self.columnNames[i]] =plot_data[self.columnNames[i]].apply(int,base=16)
                            
        else:                                                           # if no hex flag check if the data has been converted and set as float, if not set as int
            if self.convert_flag:
                plot_data = plot_data.astype(float)
            else:
                plot_data = plot_data.astype(int)
        print(plot_data)                                                # print data frame to be plotted
        for i in range(plot_data.shape[1]):
            plt.figure(str(self.columnNames[i]))
            plot_data.loc[:,self.columnNames[i]].plot(style = "-o", markersize= 1, linewidth = 0.5)    # plot each column of the dataframe with dots as data points and lines connecting them
            plt.legend(loc='upper right')

        
    # Method for plotting instantaneous data
    def mkGraph_inst(self):
        plot_data = self.pdData                                         # Create temp dataframe
        plot_data = plot_data.drop(columns='Time')                      # drop time columns
        plot_data = plot_data.drop(columns='Time_r')
        plot_data = plot_data.astype(str)                               # convert data to string
        if self.hexflag:                                                # check hexflag 
            for i in range(plot_data.shape[1]):
                plot_data[self.columnNames[i]] =plot_data[self.columnNames[i]].apply(int,base=16)
                
        else:                                                           # if no hex flag check if the data has been converted and set as float, if not set as int
            if self.convert_flag:
                plot_data = plot_data.astype(float)
            else:
                plot_data = plot_data.astype(int)
        print(plot_data)                                                # print data frame
        plot_data.plot(style = "-o", markersize= 1, linewidth = 0.5)    # plot data frame
        plt.legend(loc='upper right')

        
    # Method for saving data fram as a compressed CSV file
    def save_compress(self,flag):
        name = self.filename.split('.')                                                         # Strip file extensions 
        name = name[0]
        #print(self.pdData.to_string())
        self.pdData[self.columnNames[:-2]] = self.pdData[self.columnNames[:-2]].astype(str)     # Convert data to integer type
        if self.hexflag:
            for i in range(self.pdData.shape[1]-2):
                self.pdData[self.columnNames[i]] =self.pdData[self.columnNames[i]].apply(int,base=16)
        else:
            self.pdData[self.columnNames[:-2]] = self.pdData[self.columnNames[:-2]].astype(np.float32)
        if flag == "zip":
            self.pdData.to_csv(name+'New.csv.zip',index =False, compression = "zip")                        # If flag is 'zip' use zip compression  
        elif flag == "gzip":
            self.pdData.to_csv(name+'New.csv.gz',index =False, compression = "gzip")                        # If flag is 'gzip' use gzip compression

    # Method for retirving compressed CSV data into a dataframe (requires a dataframe object frist)
    def open_csv(self, filename):
        self.pdData = pd.read_csv(filename)                                     # read in csv infering compression
        self.filename = filename                                                # set filename as compressed filename
        self.columnNames = list(self.pdData.columns.values)                     # Save column names to object
        self.pdData["Time"] = pd.to_datetime(self.pdData["Time"],format='%Y-%m-%d %H:%M:%S', errors = 'coerce')       # convert time columns to date time types
        self.pdData["Time_r"] = pd.to_datetime(self.pdData["Time_r"],format='%Y-%m-%d %H:%M:%S', errors = 'coerce')
        
        self.convert_flag = True                                                # Ensure converted data is handeled when plotting

    # Method for joining datafiles into one dataframe 
    def join_data_text(self,filelist,outfilename, mkwidth = None, mkwidth_t = None, mkdepth = None):

        if self.pdData is not None:                                                         # check if a data frame aleardy exists
            self.pdBigData = self.pdData                                                    # set current dataframe to placeholder
            self.pdData = None
            for name in filelist:
                self.filename = name                                                        # loop over files, mkdata() and appened to placholder
                print(self.filename)
                self.pdData = None
                self.mkdata(width = mkwidth, width_t = mkwidth_t, depth = mkdepth)
                self.pdBigData = pd.concat([self.pdBigData,self.pdData], ignore_index = True)   
            self.filename = outfilename                                                     # save outfilename
            self.pdData = self.pdBigData                                                    # set placholder back to normal dataframe for other methods.
        else:
            self.filename = filelist[0]                                                     # make inital dataframe from first file
            self.mkdata()
            self.pdBigData= self.pdData
            self.pdData = None
            for name in filelist:
                if name == self.filename: continue                                          # Loop over names and append data frames togeteher
                self.filename = name
                print(self.filename)
                self.mkdata(width = mkwidth, width_t = mkwidth_t, depth = mkdepth)
                self.pdBigData = pd.concat([self.pdBigData,self.pdData], ignore_index = True)
                self.pdData = None
            print(self.pdBigData)
            self.filename = outfilename                                                     # set outfile name and set placeholder as the objects main dataframe 
            self.pdData = self.pdBigData

    # Method for converting the channel into usable data
    def Convert_channel(self,channel, scale_factor):
        self.convert_flag = True
        #avg = self.pdData[channel].mean()
        #factor = avg/scale_factor
        self.pdData[channel] = (self.pdData[channel].astype(float))*scale_factor            # Multiply the data by the scaling factor provided
        #print(factor)

    # Method for plotting specific columns of data into subplots with axis info and titles 
    def Subplot_data(self,columns, method = 'Time_real', fontsize = 18,legendsize = 10, yaxis = 'yaxis', xaxis = 'Date and Time', ylabels = None, ylim = None):

        plt.rcParams.update({'font.size': fontsize})                                # adjust fontzise
        f, axes = plt.subplots(len(columns),1, sharex = True, figsize = (20,10))    # Create number of subplot figures based on the passed column list

        if ylabels == None:
            ylabels = columns                                               # If labels not defined use pased column names   

        if method == 'Time_real':                                           # If using only timestamped sections
            plot_data = self.pdData.drop(columns='Time')                    # Drop crontructed date time column 
            plot_data = plot_data[plot_data.Time_r.notnull()]               # remove rows with null date time stamps
            plot_data = plot_data.set_index('Time_r')                       # set index as date time stamps
            
        elif method == 'Time_all':
            plot_data = self.pdData.set_index('Time')                       # Create temp data frame and set index to contructed date time stamps
            plot_data = plot_data.drop(columns='Time_r')                    # Drop real date time stamps from the set

        else:                                                               # handle error in method
            print("Unavailable method, Options are:")
            print("'Time_real'\t to plot with EDM time stamps\n'Time_all'\t to plot with added time stamps and all data")
            return
        
        plot_data = plot_data.astype(str)                                   # convert data to string type
        if self.hexflag:                                                    # check hexflag
            for i in range(plot_data.shape[1]):
                plot_data[self.columnNames[i]] =plot_data[self.columnNames[i]].apply(int,base=16)
                                                                            
        else:                                                               # if no hex flag check if the data has been converted and set as float, if not set as int
            if self.convert_flag:
                plot_data = plot_data[:-2].astype(float)
            else:
                plot_data = plot_data.astype(int)
        print(plot_data)                                                # print data frame to be plotted

        for k in range(len(columns)):
            plot_data[columns[k]].plot(ax = axes[k], style = "-o", markersize= 1, linewidth = 0.5, ylabel = ylabels[k])         # For length of columns plot each column on a separate axis 
            axes[k].legend(loc = 'upper right',prop={'size': legendsize})                                                       # Set legend location and size
            if ylim is not None and ylim[k][0] is not None:                                                                     # If y-axis limist are provided set them per subplot 
                axes[k].set_ylim(ylim[k])
            
        plt.xlabel("")
        f.supylabel(yaxis)                                              # apply labels 
        plt.xlabel(xaxis)
        
    # Method for removing rows with a None value ( only works if columns of data deacrease )
    def Remove_None(self):
        idx_arr = []
        # Uses the last column of data to check for None as number of channels should not change
        for i in range(self.pdData.shape[0]):
            if self.pdData[self.columnNames[-3]].iloc[i] == None:
                idx_arr.append(i)                                       # if last data channel is None collect index
            elif self.pdData[self.columnNames[-3]].iloc[i] == '':
                idx_arr.append(i)                                       # if last data channel is '' colelct index
        #print(len(idx_arr))
        self.pdData.drop(idx_arr, axis = 0, inplace = True)             # drop colelcted indexes from the dataframe
        self.pdData.reset_index(drop=True, inplace = True)              # reset numerical index              
        #print(self.pdData)
        pass

    # Method that provides a histogram of row sizes in item number (number of channels + date)
    # Useful for a visual assesment, corosponding bins and counts are printed to the terminal
    # Only works on datasets converted from a data file not a csv
    def Histogram_data(self):
        plt.figure()
        print(np.histogram_bin_edges(self.histogram_arr_depth[1:],bins = list(range(max(self.histogram_arr_depth)+3))))
        counts_w, bins_w = np.histogram(self.histogram_arr_width, bins = list(range(max(self.histogram_arr_width)+3)))          # histogram width of data (column number consistency)
        plt.bar(bins_w[:-1], height=counts_w)     # plot histogram
        print(bins_w)                               # print bins and counts to terminal 
        print(counts_w)
        print()
        plt.figure("histogram of page length")
        counts_d, bins_d = np.histogram(self.histogram_arr_depth[1:], bins = list(range(max(self.histogram_arr_depth)+3)))      # histogram of rows between date stamps 
        plt.bar(bins_d[:-1], height=counts_d)     # plot histogram
        print(bins_d)                               # print bins and counts to terminal
        print(counts_d)
        pass

    # Method for collecting all the filenames with a given extension and path to directory useful for the join method.
    def collect_files(self,extension = ".txt",directory = ""):
        return sorted(glob.glob(directory+'*'+extension))

    # Method for plotting several columns on one plot with 2 yaxis.
    def single_plot_2y(self,axis1, axis2, colours, method = 'Time_real', xaxis = "time", yaxis ="data",yaxis2 = "data2", legendsize = 10):

        plt.rcParams.update({'font.size': 12})                              # Adjust fontsize
        len1 = len(axis1)                                                   # get number of lines per axis
        len2 = len(axis2)
        if method == 'Time_real':                                           # If using only timestamped sections
            plot_data = self.pdData.drop(columns='Time')                    # Drop crontructed date time column 
            plot_data = plot_data[plot_data.Time_r.notnull()]               # remove rows with null date time stamps
            plot_data = plot_data.drop_duplicates()                         # remove duplicate rows from the data fram from overlapping data.
            plot_data = plot_data.set_index('Time_r')                       # set index as date time stamps
            fig,ax = plt.subplots()                                         # Create a Subplot
            ax.set_prop_cycle(color=colours[0:len1])                        # Set colour cycle to choose the first number of colours from the provided list
            ax.plot(plot_data[axis1], marker= "o",markersize = 2)           # Plot lines passed from axis1 on axis ax       
            ax.set_xlabel(xaxis)                                            # Apply x and y lables
            ax.set_ylabel(yaxis)
            ax.legend(axis1, loc = 'upper left',prop={'size': legendsize})  # Apply legend next to the related axis 
            ax2 = ax.twinx()                                                # Create second y-axis
            ax2.set_prop_cycle(color=colours[len1:])                        # Set colour cycle to use the remaning colours 
            ax2.plot(plot_data[axis2], marker= "o",markersize = 2)          # Plot lines specified in axis2
            ax2.set_ylabel(yaxis2)                                          # Label axis
            ax2.legend(axis2, loc = 'upper right',prop={'size': legendsize})# Apply legend next to the appropritae axis 
            
        elif method == 'Time_all':
            plot_data = self.pdData.set_index('Time')                       # Create temp data frame and set index to contructed date time stamps
            plot_data = plot_data.drop_duplicates()                         # Remove duplicate rows from the data frame due to overlapping of the data files
            plot_data = plot_data.drop(columns='Time_r')                    # Drop real date time stamps from the set
            fig,ax = plt.subplots()                                         # Create subplot
            ax.set_prop_cycle(color =colours[0:len1])                       # Set colour cycle to use the first len1 colours 
            ax.plot(plot_data[axis1], marker= "o",markersize = 2)           # Plot axis1 lines 
            ax.set_xlabel(xaxis)                                            # Apply x and y1 labels
            ax.set_ylabel(yaxis)
            ax.legend(axis1,loc = 'upper left',prop={'size': legendsize})   # Apply legend for axis1 next to appropriate axis
            ax2 = ax.twinx()                                                # Create second y-axis
            ax2.set_prop_cycle(color =colours[len1:])                       # Set colour cycle to use the remaing colours provided
            ax2.plot(plot_data[axis2], marker= "o",markersize = 2)          # Plot the axis2 lines on the second y-axis 
            ax2.set_ylabel(yaxis2)                                          # Label second y-axis 
            ax2.legend(axis2, loc = 'upper right',prop={'size': legendsize})# Apply legend next to the appropritae axis 

        else:                                                               # handle error in method
            print("Unavailable method, Options are:")
            print("'Time_real'\t to plot with EDM time stamps\n'Time_all'\t to plot with added time stamps and all data")
            return


    def single_plot_2y_inst(self,axis1, axis2, colours, xaxis = "time", yaxis ="data",yaxis2 = "data2",y2lim = None, legendsize = 10,samplecut = 0,samplefact = None):

        plt.rcParams.update({'font.size': 12})                              # Adjust fontsize
        len1 = len(axis1)                                                   # get number of lines per axis
        len2 = len(axis2)

        plot_data = self.pdData.drop(columns='Time')                    # Drop crontructed date time column 
        plot_data = plot_data.drop(columns = 'Time_r')                  # Drop real time column 
        plot_data = plot_data.iloc[samplecut:]                          # Select data starting from the specified cut
        plot_data = plot_data.reset_index()                             # reset the data frame index ( for converting the samples to time )
        if samplefact is not None:                                      # If a conversion factor has been provided
            plot_data['temp']= plot_data.index                          # Copy the index
            plot_data['temp'] = plot_data['temp']*samplefact            # Apply the conversion to the temp column 
            plot_data = plot_data.set_index('temp')                     # Ste temp coloumn as the index
        plot_data = plot_data.astype(str)                               # convert data to string
        if self.hexflag:                                                # check hexflag 
            for i in range(plot_data.shape[1]):
                plot_data[self.columnNames[i]] =plot_data[self.columnNames[i]].apply(int,base=16)
                
        else:                                                           # if no hex flag check if the data has been converted and set as float, if not set as int
            if self.convert_flag:
                plot_data = plot_data.astype(float)
            else:
                plot_data = plot_data.astype(int)
        fig,ax = plt.subplots()                                         # Create a Subplot
        ax.set_prop_cycle(color=colours[0:len1])                        # Set colour cycle to choose the first number of colours from the provided list
        ax.plot(plot_data[axis1],marker= "o" ,markersize = 2)           # Plot lines passed from axis1 on axis ax       
        ax.set_xlabel(xaxis)                                            # Apply x and y lables
        ax.set_ylabel(yaxis)
        ax.legend(axis1, loc = 'upper left',prop={'size': legendsize})  # Apply legend next to the related axis 
        ax2 = ax.twinx()                                                # Create second y-axis
        ax2.set_prop_cycle(color=colours[len1:])                        # Set colour cycle to use the remaning colours 
        ax2.plot(plot_data[axis2],marker= "o",markersize = 2)           # Plot lines specified in axis2
        ax2.set_ylabel(yaxis2)                                          # Label axis
        ax2.legend(axis2, loc = 'upper right',prop={'size': legendsize})# Apply legend next to the appropritae axis
        if y2lim is not None:
            ax2.set_ylim(y2lim)                                         # Set yaxis 2 limits if provided 
            
# Main area testing and funtions.
if __name__ == "__main__":
    #test= Graphing("2022-10-24__07_00.txt")
    test = Graphing("PremisisPower.dta")
    #test = Graphing("BOWMANsecPerth.dta")
    #test=Graphing("2022-10-16__00_00___2022-10-20__16_00.txt")
    #test= Graphing("2022-10-24__07_00broke.txt")
    #test= Graphing("2022-10-24__07_00double.txt")
    #test = Graphing("INST_TESTs_JAP.txt")
    #test = Graphing("2022-10-28 data_bad_stamp.txt", hexflag = True)
    #test = Graphing("2022-10-18_PerthStoppage.txt")
    test.mkdata()
    #test.join_data_text(["JAP_2022-10-04.txt","2022-10-16__00_00___2022-10-20__16_00.txt","2022-10-24__07_00.txt"], "bigdata")
    #test.name_channel(["RphV","TurV","RoutSinI","RphI_in","RoutCosI","OutI_setp","Trnsf_Out","TurbF"])
    test.name_channel(["Rwatts","RVA","Swatts","SVA","Twatts","rI","sI","tI","rV","sV","tV"])
    test.Histogram_data()
    #test.Remove_None()
    #test.ext_time_d()
    #test.open_csv("2022-10-28 data_bad_stamp.csv.zip")
    #test.mkGraph_add(start_time = "2022-10-30 00:00:00")
    #test.mkGraph_all_true()
    #test.mkGraph_true(["rV","sV","tV"])
    #test.Subplot_data(["rV","sV","tV"], 'Time_all',yaxis = 'Voltage')
    #test.mkGraph_true()
    #test.mkGraph_inst()
    #test.save_compress("zip")
    plt.show()
