#-------------------------------------------------------------------------------
# Name:        Drought Indeces SPi - Rdi
# Purpose:      Drought live Greece Monitor
#
# Author:      Anastasiadis Stavros / Antonis Tsorvas
#
# Created:     13/09/2013
# Copyright:   (c) Anastasiadis Stavros 2013
#              (c) Tzorvas Konstantinos Antonis 2013
# Licence:      MIT
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Imports
import matplotlib
matplotlib.use('Agg')
import scipy.stats as ss
import matplotlib.pylab as plt
import calendar
import numpy as np
import matplotlib.mlab as mlab
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PIL import Image
#-------------------------------------------------------------------------------
# Custion Defs
def spi_calc(spi_input_data):
    #SPI general Calculation function
    fit_k,fit_loc,fit_theta=ss.gamma.fit(spi_input_data)
    data_cdf=ss.gamma.cdf(spi_input_data,fit_k,fit_loc,fit_theta)
    data_SPI=ss.zscore(data_cdf)
    return dict(fit_k=fit_k, fit_theta = fit_theta, Spi_result = data_SPI)



#-------------------------------------------------------------------------------
# A Random Dataset
# Dictonery with general form for ONE station: Data = {Years: Month : {Rain,Temp}
# Note: in the next steps 2 more will be added i_index and PET
#e, None], '6': [None, None], '9': [23.8, 22.3], '8': [None, None]}, 2009 : {'11': [76.9, 15.6], '10': [30.0, 19.6], '12': [216.6, 14.1], '1': [184.79999999999998, 11.7], '3': [126.6, 11.8], '2': [224.39999999999998, 10.4], '5': [10.0, 18.7], '4': [34.80000000000001, 14.8], '7': [None, None], '6': [9.6, 23.0], '9': [27.0, 21.6], '8': [0.0, 24.5]}, 2010 : {'11': [37.6, 18.2], '10': [144.2, 19.3], '12': [117.80000000000001, 14.9], '1': [156.4, 11.9], '3': [16.2, 13.9], '2': [149.59999999999997, 13.4], '5': [4.0, 20.3], '4': [1.2000000000000002, 16.9], '7': [0.2, 26.7], '6': [8.0, 24.0], '9': [8.6, 23.7], '8': [0.0, 27.6]}, 2011 : {'11': [1.6, 12.5], '10': [91.60000000000001, 17.6], '12': [140.39999999999998, 12.1], '1': [214.00000000000003, 10.7], '3': [19.8, 12.4], '2': [63.2, 12.0], '5': [4.6000000000000005, 18.7], '4': [59.00000000000001, 14.5], '7': [0.0, 26.3], '6': [3.5999999999999996, 23.7], '9': [1.2000000000000002, 23.9], '8': [0.0, 25.9]}, 2012 : {'11': [128.8, 17.3], '10': [19.2, 20.5], '12': [309.20000000000005, 12.6], '1': [102.4, 8.7], '3': [44.2, 11.9], '2': [136.2, 9.3], '5': [51.0, 19.4], '4': [54.199999999999996, 17.0], '7': [0.0, 26.9], '6': [4.2, 24.7], '9': [0.0, 22.5], '8': [0.0, 26.5]}, 2013 : {'11': [None, None], '10': [None, None], '12': [None, None], '1': [286.6, 11.3], '3': [60.39999999999999, 14.4], '2': [174.4, 12.2], '5': [7.8, 20.8], '4': [22.200000000000003, 16.6], '7': [None, None], '6': [0.2, 23.4], '9': [None, None], '8': [None, None]}}
def run(appfolder, stationName, data, userid):
    try:
        userid = str(userid)
        print appfolder+'static/usercharts/'+userid+'.png'
        Data={}
        for k,v in data.iteritems():
            Data[int(k)] = {}
            for a,b in v.iteritems():
                Data[int(k)][int(a)]= map(lambda x:x if x!=None else 0,b)

        Years = Data.keys() # My Index with Years
        im = Image.open(appfolder+'static/images/logo.jpg')
        height = im.size[1]
        # We need a float array between 0-1, rather than
        # a uint8 array between 0-255
        im = np.array(im).astype(np.float) / 255
        #Exaple how to get Rain or Temp for my Data
        #print "Example:  01/1956 Rain And Temp"
        #print "Data[2008][1][0] : {}".format( Data[1956][1][0])
        #print "Data[2009][1][1] : {}" .format( Data[1956][1][1])

        #-------------------------------------------------------------------------------
        # Calculation for Thronwaite Potential Evapotranspiration Formula
        # FinalData:  Data = {Year:Month:[Rain,Temp,i_index,PET}
        #-------------------------------------------------------------------------------
        #-------------------------------------------------------------------------------
        # FINAL DATASET IS READY FOR CALC SPI AND RDI
        #-------------------------------------------------------------------------------
        # Get Special Rain and Rain/PET  DataSet :
        Rain1_data  = []
        Rain3_data  = []
        Rain6_data  = []
        Rain12_data = []

        for Year in Years:
            #Rain1
            for i in [1,2,3,4,5,6,7,8,9,10,11,12]:
                Rain1_data.append(Data[Year][i][0])
            #Rain3 Selected Months
            Months= [[1,2,3],[4,5,6],[7,8,9],[10,11,12]] # Every 3 Months Selections

            for month in Months:
                sum_rain3 = 0 # Loop for Summing
                for i in [0,1,2]:
                    sum_rain3 = sum_rain3+Data[Year][month[i]][0] # Selected Values
                    #print Year,month[i],sum_rain3 #Debug
                Rain3_data.append(sum_rain3)
            #Rain 6 Selected
            Months= [[1,2,3,4,5,6],[7,8,9,10,11,12]]
            for month in Months:
                sum_rain6 = 0
                for i in [0,1,2,3,4,5]:
                    sum_rain6 = sum_rain6+Data[Year][month[i]][0]
                Rain6_data.append(sum_rain6)
            #Rain12 Selected not so pythonic way
            Months= [[1,2,3,4,5,6,7,8,9,10,11,12]]
            for month in Months:
                sum_rain12 = 0
                for i in [0,1,2,3,4,5,6,7,8,9,10,11]:
                    sum_rain12 = sum_rain12+Data[Year][month[i]][0]
                Rain12_data.append(sum_rain12)
        #-------------------------------------------------------------------------------------------
        # Datasets For Spi Analusis  - YOU NEED TO TEST FOR RANDOM NULL VALUES!!!
        DataSPi={"Spi1":Rain1_data,"Spi3":Rain3_data,"Spi6":Rain6_data,"Spi12":Rain12_data}

        #-------------------------------------------------------------------------------------------
        #         RESULTS
        # Note : Problem with RDI (Cant figure out yet)
        #-------------------------------------------------------------------------------------------
        #THIS THE OUTPUT YOU NEED FOR THE WEB APP -- Spi diffferent time Span Resulsv
        SPIresults = {"Spi1": spi_calc(DataSPi["Spi1"]),"Spi3": spi_calc(DataSPi["Spi3"]),"Spi6": spi_calc(DataSPi["Spi6"]),"Spi12": spi_calc(DataSPi["Spi12"])}


        #-------------------------------------------------------------------------------------------
        #          Charts
        #-------------------------------------------------------------------------------------------
        StationName = stationName
        MinYear=min(Years)
        MaxYear=max(Years)
        KeysSpi = SPIresults.keys()
        # Spi1 and Rdi1 Chart-------------------------------------------------------------------------------------------
        fig = plt.figure(figsize=(6*3.13,4*3.13))
        plt.subplot(211)
        plt.axhspan(0, -0.8, facecolor='0.5', alpha=0.5,color ='yellowgreen',linewidth = True)
        plt.axhspan(-0.8, -1.3, facecolor='0.5', alpha=0.5,color ='yellow',linewidth = True)
        plt.axhspan(-1.3, -1.6, facecolor='0.5', alpha=0.5,color ='goldenrod',linewidth = True)
        plt.axhspan(-1.6, -2, facecolor='0.5', alpha=0.5,color ='r',linewidth = True)
        plt.axhspan(-2, -3, facecolor='0.5', alpha=0.5,color ='darkred',linewidth = True)
        Spi1= SPIresults["Spi1"]['Spi_result']
        n=len(Spi1)
        ind = np.arange(n)
        width = 0.40
        rects1 = plt.bar(ind, Spi1, width, color='b', label='Spi ')
        plt.ylabel('Drought Index - std units')
        plt.title('{} {} Drought Propagation Chart for The Period {} - {}'.format('[1 month]', StationName,MinYear,MaxYear))
        #Need to search in net , convert list to list of str
        xYears = []
        for Year in Years:
            xYears.append(str(Year))
        myTicks = range(0,n,12)
        plt.xticks(myTicks,xYears,rotation ="vertical")
        plt.legend(bbox_to_anchor=(1.025, 1), loc=2, borderaxespad=0.)
        plt.xlim(xmax = n)
        plt.ylim([-3,3])
        plt.text( len(Spi1), 2.5, 'Wet Conditions', rotation=90)
        plt.text( len(Spi1), -0.5, 'Dry Conditions', rotation=90)
        plt.subplot(212)
        plt.scatter(Spi1,Rain1_data,label='Spi ')
        plt.legend(bbox_to_anchor=(1.025, 1), loc=2, borderaxespad=0.)
        plt.xlabel("Drought Index")
        plt.ylabel("Rainfall (mm)")
        plt.grid()
        fig.figimage(im, 0)
        #plt.show()
        #return [os.path.join(os.getcwd(), f) for f in os.listdir(os.getcwd())]

        plt.savefig(appfolder+'static/usercharts/'
                            +stationName+'SPI_1month_'+userid+'.png')
        # <--------------------------------------------PIC ANTONIS
        plt.close()
        # Note some info inside the chart will be added later
        # Spi3 and Rdi3 Chart-------------------------------------------------------------------------------------------
        Spi3= SPIresults["Spi3"]['Spi_result']
        plt.figure(figsize=(6*3.13,4*3.13))
        plt.subplot(211)
        plt.axhspan(0, -0.8, facecolor='0.5', alpha=0.5,color ='yellowgreen',linewidth = True)
        plt.axhspan(-0.8, -1.3, facecolor='0.5', alpha=0.5,color ='yellow',linewidth = True)
        plt.axhspan(-1.3, -1.6, facecolor='0.5', alpha=0.5,color ='goldenrod',linewidth = True)
        plt.axhspan(-1.6, -2, facecolor='0.5', alpha=0.5,color ='r',linewidth = True)
        plt.axhspan(-2, -3, facecolor='0.5', alpha=0.5,color ='darkred',linewidth = True)
        n=len(Spi3)
        ind = np.arange(n)
        width = 0.40
        rects1 = plt.bar(ind, Spi3, width, color='b', label='Spi ')
        plt.ylabel('Drought Index - std units')
        plt.title('{} {} Drought Propagation Chart for The Period {} - {}'.format('[3 Month]', StationName,MinYear,MaxYear))
        #Need to search in net , convert list to list of str
        xYears = []
        for Year in Years:
            xYears.append(str(Year))
        myTicks = range(0,n,4)
        plt.xticks(myTicks,xYears,rotation='vertical')
        plt.legend(bbox_to_anchor=(1.025, 1), loc=2, borderaxespad=0.)
        plt.xlim(xmax = n)
        plt.ylim([-3,3])
        plt.text( len(Spi3), 2.5, 'Wet Conditions', rotation=90)
        plt.text( len(Spi3), -0.5, 'Dry Conditions', rotation=90)
        plt.grid()
        #plt.show()
        plt.subplot(212)
        plt.scatter(Spi3,Rain3_data,label='Spi ')
        plt.legend(bbox_to_anchor=(1.025, 1), loc=2, borderaxespad=0.)
        plt.xlabel("Drought Index")
        plt.ylabel("Rainfall (mm)")
        plt.savefig(appfolder+'static/usercharts/'
                            + stationName+'SPI_3month_'+userid+'.png')
        plt.close()

        # Spi6 and Rdi6 Chart-------------------------------------------------------------------------------------------
        plt.figure(figsize=(6*3.13,4*3.13))
        plt.subplot(211)
        Spi6= SPIresults["Spi6"]['Spi_result']
        plt.axhspan(0, -0.8, facecolor='0.5', alpha=0.5,color ='yellowgreen',linewidth = True)
        plt.axhspan(-0.8, -1.3, facecolor='0.5', alpha=0.5,color ='yellow',linewidth = True)
        plt.axhspan(-1.3, -1.6, facecolor='0.5', alpha=0.5,color ='goldenrod',linewidth = True)
        plt.axhspan(-1.6, -2, facecolor='0.5', alpha=0.5,color ='r',linewidth = True)
        plt.axhspan(-2, -3, facecolor='0.5', alpha=0.5,color ='darkred',linewidth = True)
        n=len(Spi6)
        ind = np.arange(n)
        width = 0.40
        rects1 = plt.bar(ind, Spi6, width, color='b', label='Spi')
        plt.ylabel('Drought Index - std units')
        plt.title('{} {} Drought Propagation Chart for The Period {} - {}'.format('[6 Month]', StationName,MinYear,MaxYear))
        #Need to search in net , convert list to list of str
        xYears = []
        for Year in Years:
            xYears.append(str(Year))
        myTicks = range(0,n,2)
        plt.xticks(myTicks,xYears,rotation='vertical')
        plt.legend(bbox_to_anchor=(1.025, 1), loc=2, borderaxespad=0.)
        plt.xlim(xmax = n)
        plt.ylim([-3,3])
        plt.grid()
        plt.text( len(Spi6) , 2.5, 'Wet Conditions', rotation=90)
        plt.text( len(Spi6) , -0.5, 'Dry Conditions', rotation=90)
        #plt.show()
        plt.subplot(212)
        plt.scatter(Spi6,Rain6_data,label='Spi ')
        plt.legend(bbox_to_anchor=(1.025, 1), loc=2, borderaxespad=0.)
        plt.xlabel("Drought Index")
        plt.ylabel("Rainfall (mm)")
        plt.grid()
        plt.savefig(appfolder+'static/usercharts/'
                            +stationName+'SPI_6month_'+userid+'.png')
        plt.close()
        # Spi12 and Rdi12 Chart-------------------------------------------------------------------------------------------
        Spi12= SPIresults["Spi12"]['Spi_result']
        plt.figure(figsize=(6*3.13,4*3.13))
        plt.subplot(211)
        n=len(Spi12)
        ind = np.arange(n)
        width = 0.40
        plt.axhspan(0, -0.8, facecolor='0.5', alpha=0.5,color ='yellowgreen',linewidth = True)
        plt.axhspan(-0.8, -1.3, facecolor='0.5', alpha=0.5,color ='yellow',linewidth = True)
        plt.axhspan(-1.3, -1.6, facecolor='0.5', alpha=0.5,color ='goldenrod',linewidth = True)
        plt.axhspan(-1.6, -2, facecolor='0.5', alpha=0.5,color ='r',linewidth = True)
        plt.axhspan(-2, -3, facecolor='0.5', alpha=0.5,color ='darkred',linewidth = True)
        rects1 = plt.bar(ind, Spi12, width, color='b', label='Spi ')
        plt.ylabel('Drought Index - std units')
        plt.title('{} {} Drought Propagation Chart for The Period {} - {}'.format('[12 Month]', StationName,MinYear,MaxYear))
        #Need to search in net , convert list to list of str
        xYears = []
        for Year in Years:
            xYears.append(str(Year))
        myTicks=range(0,n)
        plt.xticks(myTicks,xYears,rotation='vertical')
        plt.legend(bbox_to_anchor=(1.025, 1), loc=2, borderaxespad=0.)
        plt.xlim(xmax = n)
        plt.ylim([-3,3])
        plt.grid()
        plt.text( len(Spi12), 2.5, 'Wet Conditions', rotation=90)
        plt.text( len(Spi12), -0.5, 'Dry Conditions', rotation=90)
        #plt.show()
        plt.subplot(212)
        plt.scatter(Spi12,Rain12_data,label='Spi ')
        plt.legend(bbox_to_anchor=(1.025, 1), loc=2, borderaxespad=0.)
        plt.xlabel("Drought Index")
        plt.ylabel("Rainfall (mm)")
        plt.grid()
        plt.savefig(appfolder+'static/usercharts/'
                            +stationName+'SPI_12month_'+userid+'.png')
        plt.close()
        print "Charts Update Ending"
    except Exception, e:
        print "Drought Error:", e.message, e.args
        #-------------------------------------------------------------------------------------------
