#!/bin/env python
# add your header here
#
"""Due March 27, 2020
Created on Fri Mar 27 12:31:27 2020
by Hannah Walcek
Assignment 09 - Automated Data Quality Checking with Python

This program uses DataQualityChecking.txt as input and goes through 4 data 
quality checks: removing no data values, checking for gross errors, swapping 
max temp and min temp when max temp is less than min temp, and checking for 
daily temperature range exceedance. It also produces plots of precipitation, 
max temp, min temp and wind speed before and after cleaning.
"""
import pandas as pd
import numpy as np

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""
    
    # add your code here
    nochange = DataDF.isna() #counting na values
    totalnochange = nochange.sum() #total na values
    DataDF=DataDF.replace(-999, np.NaN) #replacing -999 with NaN
    
    ReplacedValuesDF.loc["1. No Data"] = DataDF.isna().sum() -totalnochange
    
    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    # add your code here
    nochange = DataDF.isna()
    totalnochange = nochange.sum()
    
    #Precipitation gross errors
    range = 0
    for x in DataDF.index:
        if  (25 < DataDF.loc[x, 'Precip']):
            DataDF.loc[x, 'Precip'] = np.NaN
            range = range + 1
    range = 0
    for x in DataDF.index:
        if  (DataDF.loc[x, 'Precip'] < 0):
            DataDF.loc[x, 'Precip'] = np.NaN
            range = range + 1
    
    #Max Temperature gross errors
    range = 0
    for x in DataDF.index:
        if  (35 < DataDF.loc[x, 'Max Temp']):
            DataDF.loc[x, 'Max Temp'] = np.NaN
            range = range + 1
    range = 0
    for x in DataDF.index:
        if  (DataDF.loc[x, 'Max Temp'] < -25):
            DataDF.loc[x, 'Max Temp'] = np.NaN
            range = range + 1
    
    #Min Temperature gross errors
    range = 0
    for x in DataDF.index:
        if  (35 < DataDF.loc[x, 'Min Temp']):
            DataDF.loc[x, 'Min Temp'] = np.NaN
            range = range + 1
    range = 0
    for x in DataDF.index:
        if  (DataDF.loc[x, 'Min Temp'] < -25):
            DataDF.loc[x, 'Min Temp'] = np.NaN
            range = range + 1
    
    #Wind Speed gross errors
    range = 0
    for x in DataDF.index:
        if  (10 < DataDF.loc[x, 'Wind Speed']):
            DataDF.loc[x, 'Wind Speed'] = np.NaN
            range = range + 1
    range = 0
    for x in DataDF.index:
        if  (DataDF.loc[x, 'Wind Speed'] < 0):
            DataDF.loc[x, 'Wind Speed'] = np.NaN
            range = range + 1
            
    ReplacedValuesDF.loc["2. Gross Error",:] = DataDF.isna().sum() - totalnochange
    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # add your code here
    #columns for indexing
    cols = ["Min Temp", "Max Temp"]
    #indices where Min Temp is greater than Max Temp
    ixs = DataDF['Min Temp'].gt(DataDF['Max Temp'])
    #where ixs is True, values are swapped
    DataDF.loc[ixs, cols] = DataDF.loc[ixs, cols].reindex(columns=cols[::-1]).values
    total = ixs[ixs].index #where ixs is True
    ReplacedValuesDF.loc["3. Swapped",["Max Temp", "Min Temp"]] = len(total)
    
    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # add your code here
    nochange = DataDF.isna()
    totalnochange = nochange.sum()
    
    range = 0
    for x in DataDF.index:
        if  ((DataDF.loc[x, 'Max Temp'] - DataDF.loc[x, 'Min Temp']) > 25): #where difference is greater than 25
            DataDF.loc[x, 'Max Temp'] = np.NaN #replace Max Temp with NaN
            DataDF.loc[x, 'Min Temp'] = np.NaN #replace Min Temp with NaN
            range = range + 1
    
    ReplacedValuesDF.loc["4. Range Fail",:] = DataDF.isna().sum() - totalnochange
    return( DataDF, ReplacedValuesDF )
    

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    
    #plot before and after data  
    import matplotlib.pyplot as plt
    
    #creating RawData dataframe to plot
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']
    RawData = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                             delimiter=r"\s+",parse_dates=[0])
    RawData = RawData.set_index('Date')
    
    #plot precip
    plot1=plt.figure()
    ax1=plot1.add_subplot(111)
    ax1.scatter(x=DataDF.index.values, y=RawData['Precip'], marker='.', label= "Raw Data", color='red') #plot raw
    ax1.scatter(x=DataDF.index.values, y=DataDF['Precip'], marker='.', label= "Clean Data", color = 'blue') #plot clean
    plt.xlabel('Time')
    plt.ylabel('Precipitation (mm)')
    plt.title('Daily Precipitation')
    plt.legend(loc = 'lower left')
    plt.savefig('precip.png')
    
    #plot Max Temp
    plot2=plt.figure()
    ax2=plot2.add_subplot(111)
    ax2.scatter(x=DataDF.index.values, y=RawData['Max Temp'], marker='.', label= "Raw Data", color='red') #plot raw
    ax2.scatter(x=DataDF.index.values, y=DataDF['Max Temp'], marker='.', label= "Clean Data", color = 'blue') #plot clean
    plt.xlabel('Time')
    plt.ylabel('Max Temp in Celsius')
    plt.title('Daily Maximum Temperature')
    plt.legend(loc = 'lower left')
    plt.savefig('max_temp.png')
    
    #plot Min Temp
    plot3=plt.figure()
    ax3=plot3.add_subplot(111)
    ax3.scatter(x=DataDF.index.values, y=RawData['Min Temp'], marker='.', label= "Raw Data", color='red') #plot raw
    ax3.scatter(x=DataDF.index.values, y=DataDF['Min Temp'], marker='.', label= "Clean Data", color = 'blue') #plot clean
    plt.xlabel('Time')
    plt.ylabel('Min Temp in Celsius')
    plt.title('Daily Minimum Temperature')
    plt.legend(loc = 'lower left')
    plt.savefig('min_temp.png')
    
    #plot Wind Speed
    plot4=plt.figure()
    ax4=plot4.add_subplot(111)
    ax4.scatter(x=DataDF.index.values, y=RawData['Wind Speed'], marker='.', label= "Raw Data", color='red') #plot raw
    ax4.scatter(x=DataDF.index.values, y=DataDF['Wind Speed'], marker='.', label= "Clean Data", color = 'blue') #plot clean
    plt.xlabel('Time')
    plt.ylabel('Wind Speed (m/s)')
    plt.title('Daily Wind Speed')
    plt.legend(loc = 'lower left')
    plt.savefig('windspeed.png')
    
    #exporting DataDF to text file
    DataDF.to_csv('DataQualityCheckingClean.txt', header=False, index='Date', sep = ' ')
    #exporting ReplacedValuesDF to text file
    ReplacedValuesDF.to_csv('Checks.txt', header=True, index=True, sep = '\t')