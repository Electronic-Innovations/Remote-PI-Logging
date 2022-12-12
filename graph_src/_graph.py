'''
Operating script for the EDM data graphing utility in python. More information about how the graphing and data
    analysis functions operate can be found in example.py and Graph.py.

This script can be modified to utilise the graphing utility by changing the Configuration parameters. These are described below.

Notes:

For efficiency after sucesfully joining and plotting data from a large number of data fie to save the dataframe to a csv,
    this has proven to be much more time efficient.


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
    # Directory containing only the data files to be used for multiple file processing (single_file = False).
    # Can also be used to select files satrting with the same text ie: "TD_SA/2022-11" to selec files in the TD_SA folder satarting with 2022-11 (Novemeber 2022)
    filedir = "path to files"
    # Type of file in directory to search for (".txt" or ".dta" only)
    filetype = ".txt"
    # If using mutilple files specify the name for the out file (if saving)
    outfile = "outfiledir/outfile"
    # If using a single file specify it 
    infile = "input data file"
    # Specify using presaved csv.zip data (will override single file and multiple file specifications)
    OpenCsv = True
    # Csv.zip file name/path
    csvfile = "csvfilename"
    # Specify if the data is in hexadecimal 
    hexfile = False
    # Specify if the data is instantaneous (heavily reduced functionality)
    intsdata = False
    # Specify if a historgram of EDM page length (rows between time stamps) and width (number of data columns) is requried 
    histogram = False
    # Specify if you wish to remove sections of data with columns smaller than the lagest from the historgam ( depreciated )
    removenone = False

    # Names of data channes recorded by the EDM in order from left to right in the file ( required for plotting )
    channel_names = ["Channel 1","Channel 2","Channel 3","Channel 4"]
    # Specify if all data should be plotted ('Time_all') or only time stamped data ('Time_real') for Subplots and 2yplot
    data_method = 'Time_all'
    # Specifiy if column Aveerages sgould be orinted to the terminal (useful for scaling)
    average = True
    # Which columns to average and print (None = all columns)
    avg_cols = None
    # Specify if data columns should be scaled 
    scaling = True
    # Provide a list of columns to be scaled (list of list if they are scaled by the same factor )
    columns = [["Channel 1"], ["Channel 2","Channel 3"], ["Channel 4"]]
    # A list of scaling factors to be multiplied by the values in the columns
    scale_factors = [scale factor 1, scale factor 2, scale factor 3]

    # Options for mkdata specify all or none 
    # Width of data (number of channels being recorded) determined by histogram leave as None if not specified
    histwidth = None
    histwidth_t = None    # (columns with time stamps)
    # Number of rows between time stamps (provided by histogram) Leave as None if not specified 
    pglen = None


    # Set to true if you wish to save the data frame as a csv
    save = False
    # Copression type ('zip' or 'gzip' only at the moment)
    compression = 'zip'


    # GRAPHING SELECTION #

    # Set to true to plot ints data ( Note: intsdata must be set to true above ) 
    Graph_ints = False
    
    # Set to true to plot instantaneous data on one plot with two axis ( Note: intsdata must be set to true above )
    Graph_2y_ints =False
    # List of channels to plot on the first y-axis
    Iaxis1 = ["Left Y-axis data"]
    # List of channels to plot on the second y-axis
    Iaxis2 = ["Right Y-axis data"]
    # Number of Time samples to skip at the start of plotting
    cut = 100294
    # Value to convert samples to time steps.
    Ifactor = 12
    # X-axis title
    Ixaxis = "X-axis Label"
    # Left yaxis title
    Iyaxis1 = "Left Y-axis label"
    # Right yaxis title
    Iyaxis2 = "Right Y-axis Label"
    # right yaxis limits
    Iyaxis2_lim = [lower right axis limit,upper right axis limit]
    # Colours for each of the data channels (must match number of plotted lines)
    Ilin_col = ['r','b']

    # Set to True to plot a single plot with only timestamped data 
    Graph_stamped = True
    # Number of plots to create (match length of lists)
    numberGS = 3
    # List of specific channels (None indicates all on one plot)
    specGS = [None, ["Channel 1","Channel 2"], "Channel 3"]
    # List of times to start plotitng for each plot (sometimes is funky)
    startGS = [None, None]

    # Set to true to plot single plots using all the available data
    Graph_all = True
    # Number of plots to create 
    numberGA = 2
    # List of specific channels (None indicates all on one plot)
    specGA = [None,"Channel 4"]
    # List of times to start plotitng for each plot (sometimes is funky)
    startGA = [None,None]

    # Set to True to produce a subplot with plots determined by the number of lists in subplotdata 
    subplot = False
    # A list of lists containg the data columns to be plotted on each subplot 
    subplotdata = [["Channel 1"],["Channel 2","Channel 3"],["Channel 4"]]
    # Labels for each yaxis of the plot ( must match the nummber of plots )
    subplot_ylabels = ["Top y label ", "Mid y label","Bottom y label"]
    # Label for the shared xaxis of the plot
    subplot_xlabel = "X axis Label"
    # Super label for the Y axis (can be left blank )
    subplot_yaxis = "Y Axis title "
    # Set of Y limits for each subplot ( must match the number of plots even if only one needs to be set ) 
    subplot_ylim = [[None, None], [200, 260], [None,None]]

    # Set to true to produce a sing plot with 2 y-axis
    ploty2 = True
    # List of columns to plot on the first y-axis
    axis1 = ["Channel 1","Channel 2"]
    # List of columns to plot on the second y-axis
    axis2 = ["Channel 3","Channel 4"]
    # Colours for each of the data channels (must match number of plotted lines)
    line_col = ["r","b","g","m"]
    # X-axis label
    xlab = "time"
    # first yaxis label
    ylab1 = "ylabel1"
    # Fist y-axis limits
    y1lim = None
    # second yaxis label 
    ylab2 = "ylabel2"
    # Second Y-axis Limits
    y2lim = None


# Appliaction section #


    
    if OpenCsv:                                                                     # Check open csv flag and open file
        obj = Graphing("", hexflag = hexfile)
        obj.open_csv(csvfile)
    else:                                                                           # If not open csv check if single file then oprn and make dataframe 
        if single_file:
            obj = Graphing(infile, hexflag = hexfile)
            obj.mkdata(width = histwidth, width_t = histwidth_t, depth = pglen)
        else:                                                                       # Otherwise assume collating several files
            obj = Graphing("", hexflag = hexfile)
            filelist = obj.collect_files(extension = filetype, directory = filedir) # Get list of files from directory and make dataframe 
            obj.join_data_text(filelist, outfile, mkwidth = histwidth, mkwidth_t = histwidth_t, mkdepth = pglen)

    obj.name_channel(channel_names)                                                 # Name channels 

    if histogram:                                                                   # If histogram selected make a histogram plot
        obj.Histogram_data()

    if removenone:                                                                  # If removing data lines smaller than the largest is selected
        obj.Remove_None()

    if average:
        obj.print_avg(avg_cols)

    if scaling:                                                                     # If Converting data run the converting data section for each data list of columns
        for idx in range(len(columns)):
            obj.Convert_channel(columns[idx],scale_factors[idx])

    if intsdata:                                                                    # Check ints flag and plot data due to which other flags are set and settings provided
        if Graph_ints:
            obj.mkGraph_inst()
        if Graph_2y_ints:
            obj.single_plot_2y_inst(Iaxis1, Iaxis2,Ilin_col, xaxis = Ixaxis, yaxis =Iyaxis1,yaxis2 = Iyaxis2, y2lim = Iyaxis2_lim, samplecut = cut,samplefact = Ifactor, legendsize = 10)
        plt.show()
        sys.exit(0)                                                                 # Show plot and exit cleanly 
        

    if data_method == 'Time_all' or Graph_all:                                      # Check if timestamps will need to be created for plotting
        obj.ext_time_d()

    if Graph_stamped:                                                               # Check if plotting data on time stamped graph, plot the specificed nummber 'numberGS' and data columns per graph 
        for idy in range(numberGS):
            obj.mkGraph_true(specific = specGS[idy], start_time = startGS[idy])

    if Graph_all:                                                                   # Check if plotting all data on a single plot (or only speceifc columns or a combination ) plot the combination
        for idz in range(numberGA):
            obj.mkGraph_add(specific = specGA[idz], start_time = startGA[idz])

    if subplot:                                                                     # Check if plotting a subplot and plot using specified config
        obj.Subplot_data(subplotdata,method = data_method, ylabels = subplot_ylabels, yaxis = subplot_yaxis, xaxis = subplot_xlabel,ylim = subplot_ylim)

    if ploty2:                                                                      # Check if plotting a 2 y-axis plot and plot using the specified configuration
        obj.single_plot_2y(axis1,axis2,line_col,method = data_method, xaixs = xlab, yaxis = ylab1, yaxis2 = ylab2, ylim1 = y1lim, ylim2 = y2lim legendsize = 10)

    if save:                                                                        # Check if saving data to a specified compression csv file.
        obj.save_compress(compression)

    
    plt.show()
    
