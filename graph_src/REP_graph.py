'''
Operating script for the EDM data graphing utility in python. More information about how the graphing and data
    analysis functions operate can be found in example.py and Graph.py.

This script can be modified to utilise the graphing utility by changing the starting parameters. These are described below.


'''

from Graph import Graphing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from math import sqrt

if __name__ == "__main__":

# Configuration parameters #


    # Data Input and dataframe building config #

    # Single data file flag set to true if only using a single data file
    single_file = True
    # Directory containing only the data files to be used for multiple file processing (single_file = False)
    filedir = "TD_SA/2022-11"
    # Type of file in directory to search for (".txt" or ".dta" only)
    filetype = ".txt"
    # If using mutilple files specify the name for the out file (if saving)
    outfile = "TD_SA/SA_Nov.txt"
    # If using a single file specify it 
    infile = "REP/PE-153 _4_0_no_DCcap_inst.dta"
    # Specify using presaved csv.zip data (will override single file and multiple file specifications)
    OpenCsv = False
    # Csv.zip file name/path
    csvfile = ""
    # Specify if the data is in hexadecimal 
    hexfile = False
    # Specify if the data is instantaneous (heavily reduced functionality)
    intsdata = True
    # Specify if a historgram of EDM page length (rows between time stamps) and width (number of data columns) is requried 
    histogram = False
    # Specify if you wish to remove sections of data with columns smaller than the lagest from the historgam ( depreciated )
    removenone = False

    # Names of data channes recorded by the EDM in order from left to right in the file ( required for plotting )
    channel_names = ["Voltage","Current"]
    # Specify if all data should be plotted ('Time_all') or only time stamped data ('Time_real') for Subplots ansd 2yplot
    data_method = 'Time_all'
    # Specify if data columns should be scaled 
    scaling = True
    # Provide a list of columns to be scaled (list of list if they are scaled by the same factor )
    columns = ["Voltage","Current"]
    # A list of scaling factors to be multiplied by the values in the columns
    scale_factors = [(245/13623)*sqrt(2), (68/4754)*sqrt(2)]

    # Set to true if you wish to save the data frame as a csv
    save = False
    # Copression type ('zip' or 'gzip' only at the moment)
    compression = 'zip'


    # GRAPHING SELECTION #

    # Set to true to plot ints data
    Graph_ints = False

    # Set to true to plot instantaneous data on one plot with two axis
    Graph_2y_ints =True
    # List of channels to plot on the first y-axis
    Iaxis1 = ["Voltage"]
    # List of channels to plot on the second y-axis
    Iaxis2 = ["Current"]

    cut = 100294
    
    Ifactor = 0.02/32
    # X-axis title
    Ixaxis = "Seconds (s)"
    # Left yaxis title
    Iyaxis1 = "Voltage (V)"
    # Right yaxis title
    Iyaxis2 = "Current (A)"
    # right yaxis limits
    Iyaxis2_lim = [-150,150]
    # Colours for each of the data channels (must match number of plotted lines)
    Ilin_col = ['r','b']
    
    # Set to True to plot a single plot with only timestamped data 
    Graph_stamped = True
    # Number of plots to create (match length of lists)
    numberGS = 2
    # List of specific channels (None indicates all on one plot)
    specGS = [None, None]
    # List of times to start plotitng for each plot (sometimes is funky)
    startGS = [None, None]

    # Set to true to plot single plots using all the available data
    Graph_all = True
    # Number of plots to create 
    numberGA = 2
    # List of specific channels (None indicates all on one plot)
    specGA = [None,None]
    # List of times to start plotitng for each plot (sometimes is funky)
    startGA = [None,None]

    # Set to True to produce a subplot with 3 plots 
    subplot = False
    # A list of lists containg the data columns to be plotted on each subplot 
    subplotdata = [["DCv-Min","DCv-MAX"],["SphV-Min","SphV-MAX","RphV-Min","RphV-MAX"],["SphI-Min","SphI-MAX","RphI-Min","RphI-MAX"]]
    # Labels for each yaxis of the plot
    subplot_ylabels = ["Volts (V)", "Volts (V)","Current (A)"]
    # Label for the shared xaxis of the plot
    subplot_xlabel = "November 2022 JAP MINE"
    # Super label for the Y axis (can be left blank )
    subplot_yaxis = "DC Converter, Mains and Out Current"

    # Set to true to produce a sing plot with 2 y-axis
    ploty2 = True
    # List of channels to plot on the first y-axis
    axis1 = ["DCv-Min","DCv-MAX"]
    # List of channels to plot on the second y-axis
    axis2 = ["SphI-Min","SphI-MAX","RphI-Min","RphI-MAX"]
    # Colours for each of the data channels (must match number of plotted lines)
    line_col = ["r","b","g","m","y","c"]
    # X-axis label
    xlab = "time"
    # first yaxis label
    ylab1 = "ylabel1"
    # second yaxis label 
    ylab2 = "ylabel2"


# Appliaction section #

    if OpenCsv:
        obj = Graphing("", hexflag = hexfile)
        obj.open_csv("TD_SA/SA_NovNew.csv.zip")
    else:
        if single_file:
            obj = Graphing(infile, hexflag = hexfile)
            obj.mkdata()
        else:
            obj = Graphing("", hexflag = hexfile)
            filelist = obj.collect_files(extension = filetype, directory = filedir)
            obj.join_data_text(filelist, outfile)

    obj.name_channel(channel_names)

    if histogram:
        obj.Histogram_data()

    if removenone:
        obj.Remove_None()

    if scaling:
        for idx in range(len(columns)):
            obj.Convert_channel(columns[idx],scale_factors[idx])

    if intsdata:
        if Graph_ints:
            obj.mkGraph_inst()
        if Graph_2y_ints:
            obj.single_plot_2y_inst(Iaxis1, Iaxis2,Ilin_col, xaxis = Ixaxis, yaxis =Iyaxis1,yaxis2 = Iyaxis2, y2lim = Iyaxis2_lim, samplecut = cut,samplefact = Ifactor, legendsize = 10)
        plt.show()
        sys.exit(0)
        

    if data_method == 'Time_all' or Graph_all:
        obj.ext_time_d()

    if Graph_stamped:
        for idy in range(numberGS):
            obj.mkGraph_true(specific = specGS[idy], start_time = startGS[idy])

    if Graph_all:
        for idz in range(numberGA):
            obj.mkGraph_add(specific = specGA[idz], start_time = startGA[idz])

    if subplot:
        obj.Subplot_data(subplotdata,method = data_method, ylabels = subplot_ylabels, yaxis = subplot_yaxis, xaxis = subplot_xlabel)

    if ploty2:
        obj.single_plot_2y(axis1,axis2,line_col,method = data_method)

    if save:
        obj.save_compress(compression)

    
    plt.show()
    
    ################################
    #For a single data file file
    
    #filename = "Placholder.txt"
    #Channel_names
    #channel_names = ["Rwatts","RVA","Swatts","SVA","Twatts","rI","sI","tI","rV","sV","tV"]

    #Create Object
    #obj = Graphing(filename, hexflag = False)

    #Make the dataframe and histogram info
    #obj.mkdata()

    #Create the histogram fig 
    #obj.Histogram_data()

    #If there are more than the expected number of recorded data widths re-run mkdata()
    #   using the width and width_t variables
    #obj.mkdata(width = highest count bin, width_t = second hights count bin)

    #histogram showed large number of sections with fewer channels therfore run
    #obj.Remove_None()

    #name channels
    #obj.name_channel(channel_names)

    #plot should work now plot all EDM timestamped data from the beginning of the data
    #obj.mkGraph_true(specific = None,start_time = None)

    #plot only rV sV and tV after 2022-09-01 00:00:00
    #obj.mkGraph_true(["rV","sV","tV"], start_time = "2022-09-01 00:00:00")

    #plot each channel individually (EDM timestamped)
    #obj.mkGraph_all_true(start_time = None)
    
    #ploting all rows of data reqires
    #obj.ext_time_d()

    #Plotting for all rows functions have tha same syntax
    #obj.mkGraph_add(specific = None,start_time = None)

    #plot only rV sV and tV after 2022-09-01 00:00:00
    #obj.mkGraph_add(["rV","sV","tV"], start_time = "2022-09-01 00:00:00")

    #plot each channel individually (EDM timestamped)
    #obj.mkGraph_all_add(start_time = None)

    # If a subplot is required for several channles
    # plot a subplot of rV sV and tV using all rows with fontsize 18 anf labelled major axis 
    #obj.Subplot_data(["rV","sV","tV"], method ='Time_all', fontsize = 18 ,yaxis = 'Voltage',xaxis = 'Date and Time')

    # If a single plot with 2 y-axis are required
    # plot a single plot with DCv-Min and DCv-MAX on the left axis in red and blue. And plot SphI-Min, SphI-MAX, RphI-Min and RphI-MAX on the right yaxis in green, magenta, yellow and cyan
    # using all the data points. Look in Graph.py for more options for labelling
    #obj.single_plot_2y(["DCv-Min","DCv-MAX"],["SphI-Min","SphI-MAX","RphI-Min","RphI-MAX"],["r","b","g","m","y","c"],method = "Time_all")

    # To save the dataframe to compressed csv using 'zip' compression
    #obj.save_compress("zip")



    ################################
    # To use a prexisting csv.zip that has been processed

    #filename = "Place Holder Zip file name"
    #obj = Graphing("")
    #obj.open_csv(filename)
    
    # Assuming all processing has been done can be plotted as above

    ################################
    # To process and INTS data file
    #filename = "Placholder.txt"
    #Channel_names
    #channel_names = ["Rwatts","RVA","Swatts","SVA","Twatts","rI","sI","tI","rV","sV","tV"]

    #Create Object
    #obj = Graphing(filename, hexflag = False)

    #Make the dataframe and histogram info
    #obj.mkdata()

    # Plot using the specific ints graph function
    #obj.mkGraph_ints()

    ################################
    #To process several files into one dataframe. Data must have the same column width

    # List of file names
    #filelist = ["fiel1, file 2"]
    # Or generate from directory
    #filelist = obj.collect_files(directory = "path", extension = ".txt/.dta")

    #Channel_names
    #channel_names = ["Rwatts","RVA","Swatts","SVA","Twatts","rI","sI","tI","rV","sV","tV"]

    # Create Object
    #obj = Graphing("TD_SA/2022-06-28_14-25.txt", hexflag = False)

    # Replacement mkdata
    #obj.join_data_text(filelist, "outfilename")
    
    # steps can now be followed as if its a single file. Note that the histogram option may be
    # inacurate as the mkdata() function is called several times in the join_data_text() function.


   
    
