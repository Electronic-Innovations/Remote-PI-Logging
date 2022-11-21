

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
    #channel_names = ["Rwatts","RVA","Swatts","SVA","Twatts","rI","sI","tI","rV","sV","tV"]

    # Create Object
    obj = Graphing("TD_SA/2022-06-28_14-25.txt", hexflag = False)
    filelist = obj.collect_files(directory = "TD_SA/")
    #obj.mkdata()
    
    #obj.Histogram_data()
    #obj.open_csv("TD_SA/SA_TEST.txtNew.csv.zip")
    # Replacement mkdata
    obj.join_data_text(filelist, "TD_SA/SA_TEST.txt")

    #obj.mkGraph_true(specific = None,start_time = None)
    obj.ext_time_d()
    #obj.mkGraph_add(specific = None,start_time = None)
    obj.save_compress("zip")
    
    # function that shows the plots. Must be called after they are created
    plt.show()
