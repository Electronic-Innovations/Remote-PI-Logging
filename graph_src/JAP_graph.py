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

if __name__ == "__main__":

# Configuration parameters #


    # Data Input and dataframe building config #

    # Single data file flag set to true if only using a single data file
    single_file = False
    # Directory containing only the data files to be used for multiple file processing (single_file = False)
    filedir = "TD_SA/2022-12"
    # Type of file in directory to search for (".txt" or ".dta" only)
    filetype = ".txt"
    # If using mutilple files specify the name for the out file (if saving)
    outfile = "TD_SA/SA_Dec.txt"
    # If using a single file specify it 
    infile = "AN_DAT/2022-12-02__06_00.txt"
    # Specify using presaved csv.zip data (will override single file and multiple file specifications)
    OpenCsv = False
    # Csv.zip file name/path
    csvfile = "TD_SA/SA_NovDecNew.csv.zip"
    # Specify if the data is in hexadecimal 
    hexfile = False
    # Specify if the data is instantaneous (heavily reduced functionality)
    intsdata = False
    # Specify if a historgram of EDM page length (rows between time stamps) and width (number of data columns) is requried 
    histogram = True
    # Specify if you wish to remove sections of data with columns smaller than the lagest from the historgam ( depreciated )
    removenone = True

    # Names of data channes recorded by the EDM in order from left to right in the file ( required for plotting )
    channel_names = ["DC-v","Sph-V","Rph-V","Rph-I","Sph-I","DCv-Min","SphV-Min","RphV-Min","RphI-Min","SphI-Min","DCv-MAX", "SphV-MAX","RphV-MAX","RphI-MAX","SphI-MAX"]
    # Specify if all data should be plotted ('Time_all') or only time stamped data ('Time_real') for Subplots ansd 2yplot
    data_method = 'Time_real'
    # Specify if data columns should be scaled 
    scaling = False
    # Provide a list of columns to be scaled (list of list if they are scaled by the same factor )
    columns = [["DCv-Min","DC-v","Sph-V","Rph-V","DCv-MAX","SphV-Min","SphV-MAX","RphV-Min","RphV-MAX"], ["Rph-I","Sph-I","RphI-Min","SphI-Min","RphI-MAX","SphI-MAX"]]
    # A list of scaling factors to be multiplied by the values in the columns
    scale_factors = [(2440/97310), 65/2322.3006944444446]
    # Width of data (number of channels being recorded) determined by histogram leave as None if not specified
    histwidth = 15
    histwidth_t = 16    # columns with dime stamps)
    # Number of rows between time stamps (provided by histogram) Leave as None if not specified 
    pglen = 8

    # Set to true if you wish to save the data frame as a csv
    save = False
    # Copression type ('zip' or 'gzip' only at the moment)
    compression = 'zip'


    # GRAPHING SELECTION #

    # Set to true to plot ints data
    Graph_ints = False
    
    # Set to true to plot instantaneous data on one plot with two axis
    Graph_2y_ints =False
    # List of channels to plot on the first y-axis
    Iaxis1 = ["Voltage"]
    # List of channels to plot on the second y-axis
    Iaxis2 = ["Current"]
    # Value to convert samples to time steps.
    Ifactor = 12
    # X-axis title
    Ixaxis = "Sample"
    # Left yaxis title
    Iyaxis1 = "Voltage (V)"
    # Right yaxis title
    Iyaxis2 = "Current (A)"
    # right yaxis limits
    Iyaxis2_lim = [-100,100]
    # Colours for each of the data channels (must match number of plotted lines)
    Ilin_col = ['r','b']

    # Set to True to plot a single plot with only timestamped data 
    Graph_stamped = False
    # Number of plots to create (match length of lists)
    numberGS = 1
    # List of specific channels (None indicates all on one plot)
    specGS = [None, None]
    # List of times to start plotitng for each plot (sometimes is funky)
    startGS = [None, None]

    # Set to true to plot single plots using all the available data
    Graph_all = True
    # Number of plots to create 
    numberGA = 1
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
    subplot_xlabel = "November-December 2022 JAP MINE"
    # Super label for the Y axis (can be left blank )
    subplot_yaxis = "Out Current, Mains and DC Converter"
    # Set of Y limits for each subplot
    subplot_ylim = [[None, None], [200, 260], [None,None]]

    # Set to true to produce a sing plot with 2 y-axis
    ploty2 = False
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
        obj.open_csv(csvfile)
    else:
        if single_file:
            obj = Graphing(infile, hexflag = hexfile)
            obj.mkdata(width = histwidth, width_t = histwidth_t, depth = pglen)
        else:
            obj = Graphing("", hexflag = hexfile)
            filelist = obj.collect_files(extension = filetype, directory = filedir)
            obj.join_data_text(filelist, outfile, mkwidth = histwidth, mkwidth_t = histwidth_t, mkdepth = pglen)

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
            obj.single_plot_2y_inst(Iaxis1, Iaxis2,Ilin_col, xaxis = Ixaxis, yaxis =Iyaxis1,yaxis2 = Iyaxis2, y2lim = Iyaxis2_lim, samplefact = Ifactor, legendsize = 10)
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
        obj.Subplot_data(subplotdata,method = data_method, ylabels = subplot_ylabels, yaxis = subplot_yaxis, xaxis = subplot_xlabel, ylim = subplot_ylim)

    if ploty2:
        obj.single_plot_2y(axis1,axis2,line_col,method = data_method)

    if save:
        obj.save_compress(compression)

    
    plt.show()
    
