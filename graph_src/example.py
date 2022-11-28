

from Graph import Graphing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":


    ################################
    #For a single data file file
    
    filename = "Placholder.txt"
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


    #######################################
    #Assorted testing



        # List of file names
    #filelist = ["file1","file2"]

    #Channel_names
    channel_names = ["DC-v","Sph-V","Rph-V","Rph-I","Sph-I","DCv-Min","SphV-Min","RphV-Min","RphI-Min","SphI-Min","DCv-MAX", "SphV-MAX","RphV-MAX","RphI-MAX","SphI-MAX"]

    # Create Object
    obj = Graphing("TD_SA/2022-11-22__05_00.txt", hexflag = False)
    #filelist = obj.collect_files(directory = "TD_SA/2022-11")
    #obj.mkdata()
    
    #obj.Histogram_data()
    obj.open_csv("TD_SA/SA_NovNew.csv.zip")
    # Replacement mkdata
    #obj.join_data_text(filelist, "TD_SA/SA_Nov.txt")
    #obj.Histogram_data()
    obj.name_channel(channel_names)
    # Converting voltages
    scale= (2440/97310)
    obj.Convert_channel(["DCv-Min","DC-v","Sph-V","Rph-V","DCv-MAX","SphV-Min","SphV-MAX","RphV-Min","RphV-MAX"],scale)
    temp =2322.3006944444446
    factor = 65/temp
    obj.Convert_channel(["Rph-I","Sph-I","RphI-Min","SphI-Min","RphI-MAX","SphI-MAX"],factor)
    #obj.mkGraph_true(specific = ["DCv-Min","DCv-MAX","SphV-Min","SphV-MAX","RphV-Min","RphV-MAX","SphI-Min","SphI-MAX","RphI-Min","RphI-MAX"],start_time = None)
    #obj.mkGraph_true()
    #obj.ext_time_d()
    #obj.mkGraph_add()
    #obj.mkGraph_add(specific = ["Rph-I"])
    #obj.mkGraph_add(specific = ["DCv-Min","DCv-MAX","SphV-Min","SphV-MAX","RphV-Min","RphV-MAX","SphI-Min","SphI-MAX","RphI-Min","RphI-MAX"],start_time = None)
    obj.Subplot_data([["DCv-Min","DCv-MAX"],["SphV-Min","SphV-MAX","RphV-Min","RphV-MAX"],["SphI-Min","SphI-MAX","RphI-Min","RphI-MAX"]],method = 'Time_all', ylabels = ["Volts (V)", "Volts (V)","Current (A)"], yaxis = '', xaxis = '2022-11-21 (AEST)')
    obj.single_plot_2y(["DCv-Min","DCv-MAX"],["SphI-Min","SphI-MAX","RphI-Min","RphI-MAX"],["r","b","g","m","y","c"],method = "Time_all")
    #obj.save_compress("zip")

    # function that shows the plots. Must be called after they are created
    plt.show()
