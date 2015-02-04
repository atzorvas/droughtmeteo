#-------------------------------------------------------------------------------
# Name:         Drought Algorithm
# Purpose:     	Drought live Greece Monitor
#
# Author:      	Anastasiadis Stavros / Antonis Tsorvas
#
# Created:     	13/09/2013
# Copyright:   	(c) Anastasiadis Stavros 2013
#              	(c) Tzorvas Konstantinos Antonis 2013
# Licence:     	MIT
#-------------------------------------------------------------------------------
import matplotlib
matplotlib.use('Agg')
import scipy.stats as ss
import matplotlib.pylab as plt
import calendar
import numpy as np


def spi_calc(spi_input_data):
    #SPI general Calculation function
    fit_k,fit_loc,fit_theta=ss.gamma.fit(spi_input_data)
    data_cdf=ss.gamma.cdf(spi_input_data,fit_k,fit_loc,fit_theta)
    data_SPI=ss.zscore(data_cdf)
    return dict(fit_k=fit_k, fit_theta = fit_theta, Spi_result = data_SPI)


def rdi_calc(rdi_input_data):
    #Rdi general Calculation function
    shape, loc, scale = ss.lognorm.fit(rdi_input_data)
    data_cdf = ss.lognorm.cdf(rdi_input_data,shape,loc,scale)
    data_RDI = ss.zscore(data_cdf)
    return dict(shape = shape, scale = scale, Rdi_result = data_RDI)
#def hist_data(data_in):
#    #histgramm equation
#    n, low_range, binsize, extrapoints = ss.histogram(data_in)
#    upper_range = low_range+binsize*(len(n)-1)
#    bins = np.linspace(low_range, upper_range, len(n))
#    plt.bar(bins, n, color='red')
#    plt.xlabel('X', fontsize=20)
#    plt.ylabel('number of data points in the bin', fontsize=15)
#    plt.show()

#-------------------------------------------------------------------------------
# A Random Dataset
# Dictonery with general form for ONE station: Data = {Years: Month : {Rain,Temp}
# Note: in the next steps 2 more will be added i_index and PET
#e, None], '6': [None, None], '9': [23.8, 22.3], '8': [None, None]}, 2009 : {'11': [76.9, 15.6], '10': [30.0, 19.6], '12': [216.6, 14.1], '1': [184.79999999999998, 11.7], '3': [126.6, 11.8], '2': [224.39999999999998, 10.4], '5': [10.0, 18.7], '4': [34.80000000000001, 14.8], '7': [None, None], '6': [9.6, 23.0], '9': [27.0, 21.6], '8': [0.0, 24.5]}, 2010 : {'11': [37.6, 18.2], '10': [144.2, 19.3], '12': [117.80000000000001, 14.9], '1': [156.4, 11.9], '3': [16.2, 13.9], '2': [149.59999999999997, 13.4], '5': [4.0, 20.3], '4': [1.2000000000000002, 16.9], '7': [0.2, 26.7], '6': [8.0, 24.0], '9': [8.6, 23.7], '8': [0.0, 27.6]}, 2011 : {'11': [1.6, 12.5], '10': [91.60000000000001, 17.6], '12': [140.39999999999998, 12.1], '1': [214.00000000000003, 10.7], '3': [19.8, 12.4], '2': [63.2, 12.0], '5': [4.6000000000000005, 18.7], '4': [59.00000000000001, 14.5], '7': [0.0, 26.3], '6': [3.5999999999999996, 23.7], '9': [1.2000000000000002, 23.9], '8': [0.0, 25.9]}, 2012 : {'11': [128.8, 17.3], '10': [19.2, 20.5], '12': [309.20000000000005, 12.6], '1': [102.4, 8.7], '3': [44.2, 11.9], '2': [136.2, 9.3], '5': [51.0, 19.4], '4': [54.199999999999996, 17.0], '7': [0.0, 26.9], '6': [4.2, 24.7], '9': [0.0, 22.5], '8': [0.0, 26.5]}, 2013 : {'11': [None, None], '10': [None, None], '12': [None, None], '1': [286.6, 11.3], '3': [60.39999999999999, 14.4], '2': [174.4, 12.2], '5': [7.8, 20.8], '4': [22.200000000000003, 16.6], '7': [None, None], '6': [0.2, 23.4], '9': [None, None], '8': [None, None]}}
def run(appfolder, stationName, data):
    try:
        Data={}
        for k, v in data.iteritems():
            Data[int(k)] = {}
            for a, b in v.iteritems():
                Data[int(k)][int(a)] = map(lambda x: x if x!=None else 0,b)

        print "DATA TO RUN...", Data
        Years = Data.keys() # My Index with Years
        #-------------------------------------------------------------------------------
        # Calculation for Thronwaite Potential Evapotranspiration Formula
        # FinalData:  Data = {Year:Month:[Rain,Temp,i_index,PET}
        #-------------------------------------------------------------------------------
        #Calculation i_index
        for Year in Years:
            for i in [1,2,3,4,5,6,7,8,9,10,11,12]:
                if Data[Year][i][1]>0:
                    i_index = 0.09*(Data[Year][i][1])**1.514
                else: #if Data[Year][i][1]<=0:
                    i_index = 0
                Data[Year][i].append(i_index)
        #Daylight Hour  (Just for Now) Constant =12 hour <----- THIS WILL CHANGE!!!
        N=12
        for Year in Years:
            sum_I=0
            for i in [1,2,3,4,5,6,7,8,9,10,11,12]:
                sum_I = sum_I + Data[Year][i][2]
            for i in [1,2,3,4,5,6,7,8,9,10,11,12]:
                DaysPerMonth = [31,28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                if calendar.isleap(Year) == True:
                    DaysPerMonth[1]=29
                N=12
                if Data[Year][i][1] == 0:
                    PET = 0
                else:
                    if sum_I != 0: #prevent division by zero
                        PET  = 16 * (10 * (Data[Year][i][1])/sum_I)* ( DaysPerMonth[i-1] * N/360)
                    else:
                        print stationName, Data
                        PET = 0
                if PET <= 0 :
                    Data[Year][i].append(0)
                else:
                    Data[Year][i].append(PET)
        #-------------------------------------------------------------------------------
        # FINAL DATASET IS READY FOR CALC SPI AND RDI
        #-------------------------------------------------------------------------------
        # Get Special Rain and Rain/PET  DataSet :
        rain1_data = []
        rain3_data = []
        rain6_data = []
        rain12_data = []
        rainpet1 = []
        rainpet3 = []
        rainpet6 = []
        rainpet12 = []

        for Year in Years:
            #Rain1
            for i in [1,2,3,4,5,6,7,8,9,10,11,12]:
                rain1_data.append(Data[Year][i][0])
                if Data[Year][i][3]==0:
                    rainpet1.append(0)
                else:
                    rainpet1.append(float(Data[Year][i][0])/Data[Year][i][3])
            #Rain3 Selected Months
            Months= [[1,2,3],[4,5,6],[7,8,9],[10,11,12]] # Every 3 Months Selections
            for month in Months:
                sum_rain3 = 0 # Loop for Summing
                sum_RP3 = 0
                for i in [0,1,2]:
                    sum_rain3 = sum_rain3+Data[Year][month[i]][0] # Selected Values
                    if Data[Year][month[i]][3] != 0:
                        sum_RP3 = sum_RP3 +float(Data[Year][month[i]][0])/(Data[Year][month[i]][3])
                    else:
                        sum_RP3 = sum_RP3 + 0
                rain3_data.append(sum_rain3)
                rainpet3.append(sum_RP3)
            #Rain 6 Selected
            Months= [[1,2,3,4,5,6],[7,8,9,10,11,12]]
            for month in Months:
                sum_rain6 = 0
                sum_RP6 = 0
                for i in [0,1,2,3,4,5]:
                    sum_rain6 = sum_rain6+Data[Year][month[i]][0]
                    if Data[Year][month[i]][3] !=0:
                        sum_RP6 = sum_RP6 +float(Data[Year][month[i]][0])/(Data[Year][month[i]][3])
                    else:
                        sum_RP6 = sum_RP6 + 0
                rain6_data.append(sum_rain6)
                rainpet6.append(sum_RP6)
            #Rain12 Selected not so pythonic way
            Months= [[1,2,3,4,5,6,7,8,9,10,11,12]]
            for month in Months:
                sum_rain12 = 0
                sum_RP12 = 0
                for i in [0,1,2,3,4,5,6,7,8,9,10,11]:
                    sum_rain12 = sum_rain12+Data[Year][month[i]][0]
                    if Data[Year][month[i]][3] !=0:
                        sum_RP12 = sum_RP12 +float(Data[Year][month[i]][0])/(Data[Year][month[i]][3])
                    else:
                       sum_RP12 = sum_RP12 + 0
                rain12_data.append(sum_rain12)
                rainpet12.append(sum_RP12)
        #-------------------------------------------------------------------------------------------
        # Datasets For Spi Analusis  - YOU NEED TO TEST FOR RANDOM NULL VALUES!!!
        dataspi = {"Spi1":rain1_data,"Spi3":rain3_data,"Spi6":rain6_data,"Spi12":rain12_data}
        datardi = {"Rdi1":rainpet1,"Rdi3":rainpet3,"Rdi6":rainpet6,"Rdi12":rainpet12}

        #-------------------------------------------------------------------------------------------
        #         RESULTS
        # Note : Problem with RDI (Cant figure out yet)
        #-------------------------------------------------------------------------------------------
        #THIS THE OUTPUT YOU NEED FOR THE WEB APP -- Spi diffferent time Span Resulsv
        spiresults = {"Spi1": spi_calc(dataspi["Spi1"]),"Spi3": spi_calc(dataspi["Spi3"]),"Spi6": spi_calc(dataspi["Spi6"]),"Spi12": spi_calc(dataspi["Spi12"])}
        rdiresults = {"Rdi1": rdi_calc(datardi["Rdi1"]),"Rdi3": rdi_calc(datardi["Rdi3"]),"Rdi6": rdi_calc(datardi["Rdi6"]),"Rdi12": rdi_calc(datardi["Rdi12"])}

        #-------------------------------------------------------------------------------------------
        #          Charts
        #-------------------------------------------------------------------------------------------
        stationname = stationName
        minyear=min(Years)
        maxyear=max(Years)
        keysspi = spiresults.keys()
        keysrdi = rdiresults.keys()
        # Spi1 and Rdi1 Chart-------------------------------------------------------------------------------------------
        plt.figure(figsize=(6*3.13,4*3.13))
        plt.subplot(211)
        plt.axhspan(0, -0.8, facecolor='0.5', alpha=0.5,color ='yellow',linewidth = True)
        plt.axhspan(-0.8, -1.3, facecolor='0.5', alpha=0.5,color ='orange',linewidth = True)
        plt.axhspan(-1.3, -1.6, facecolor='0.5', alpha=0.5,color ='orangered',linewidth = True)
        plt.axhspan(-1.6, -2, facecolor='0.5', alpha=0.5,color ='r',linewidth = True)
        plt.axhspan(-2, -3, facecolor='0.5', alpha=0.5,color ='maroon',linewidth = True)
        Spi1= spiresults["Spi1"]['Spi_result']
        Rdi1= rdiresults["Rdi1"]['Rdi_result']
        n=len(Spi1)
        ind = np.arange(n)
        width = 0.40
        rects1 = plt.bar(ind, Spi1, width, color='b', label='SPI ')
        rects2 = plt.bar(ind+width, Rdi1, width, color='lightblue', label='RDI ')
        plt.ylabel('Drought Index - std units')
        plt.title('{} {} Drought Propagation Chart for The Period {} - {}'.format('[1 month]', stationname,minyear,maxyear))
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
        plt.scatter(Spi1,rain1_data,label='Spi ')
        plt.scatter(Rdi1,rain1_data,c="lightblue",label='Rdi ')
        plt.legend(bbox_to_anchor=(1.025, 1), loc=2, borderaxespad=0.)
        plt.xlabel("Drought Index")
        plt.ylabel("Rainfall (mm)")
        plt.grid()
        #plt.show()
        #return [os.path.join(os.getcwd(), f) for f in os.listdir(os.getcwd())]

        plt.savefig(appfolder+'/static/charts'
                            '/'+stationName+'_1month.png')
        # <--------------------------------------------PIC ANTONIS
        plt.close()
        # Note some info inside the chart will be added later
        # Spi3 and Rdi3 Chart-------------------------------------------------------------------------------------------
        Spi3= spiresults["Spi3"]['Spi_result']
        Rdi3= rdiresults["Rdi3"]['Rdi_result']
        plt.figure(figsize=(6*3.13,4*3.13))
        plt.subplot(211)
        plt.axhspan(0, -0.8, facecolor='0.5', alpha=0.5,color ='yellow',linewidth = True)
        plt.axhspan(-0.8, -1.3, facecolor='0.5', alpha=0.5,color ='orange',linewidth = True)
        plt.axhspan(-1.3, -1.6, facecolor='0.5', alpha=0.5,color ='orangered',linewidth = True)
        plt.axhspan(-1.6, -2, facecolor='0.5', alpha=0.5,color ='r',linewidth = True)
        plt.axhspan(-2, -3, facecolor='0.5', alpha=0.5,color ='maroon',linewidth = True)
        n=len(Spi3)
        ind = np.arange(n)
        width = 0.40
        rects1 = plt.bar(ind, Spi3, width, color='b', label='SPI ')
        rects2 = plt.bar(ind + width, Rdi3, width, color='lightblue', label='RDI ')
        plt.ylabel('Drought Index - std units')
        plt.title('{} {} Drought Propagation Chart for The Period {} - {}'.format('[3 Month]', stationname,minyear,maxyear))
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
        plt.scatter(Spi3,rain3_data,label='SPI ')
        plt.scatter(Rdi3,rain3_data,c="lightblue",label='RDI ')
        plt.legend(bbox_to_anchor=(1.025, 1), loc=2, borderaxespad=0.)
        plt.xlabel("Drought Index")
        plt.ylabel("Rainfall (mm)")
        plt.grid()
        plt.savefig(appfolder+'static/charts'
                            '/'+stationName+'_3month.png')
        plt.close()

        # Spi6 and Rdi6 Chart-------------------------------------------------------------------------------------------
        plt.figure(figsize=(6*3.13,4*3.13))
        plt.subplot(211)
        Spi6= spiresults["Spi6"]['Spi_result']
        Rdi6= rdiresults["Rdi6"]['Rdi_result']
        plt.axhspan(0, -0.8, facecolor='0.5', alpha=0.5,color ='yellow',linewidth = True)
        plt.axhspan(-0.8, -1.3, facecolor='0.5', alpha=0.5,color ='orange',linewidth = True)
        plt.axhspan(-1.3, -1.6, facecolor='0.5', alpha=0.5,color ='orangered',linewidth = True)
        plt.axhspan(-1.6, -2, facecolor='0.5', alpha=0.5,color ='r',linewidth = True)
        plt.axhspan(-2, -3, facecolor='0.5', alpha=0.5,color ='maroon',linewidth = True)
        n=len(Spi6)
        ind = np.arange(n)
        width = 0.40
        rects1 = plt.bar(ind, Spi6, width, color='b', label='SPI')
        rects2 = plt.bar(ind + width, Rdi6, width, color='lightblue', label='RDI')
        plt.ylabel('Drought Index - std units')
        plt.title('{} {} Drought Propagation Chart for The Period {} - {}'.format('[6 Month]', stationname,minyear,maxyear))
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
        plt.scatter(Spi6,rain6_data,label='SPI')
        plt.scatter(Rdi6,rain6_data,c="r",label='RDI ')
        plt.legend(bbox_to_anchor=(1.025, 1), loc=2, borderaxespad=0.)
        plt.xlabel("Drought Index")
        plt.ylabel("Rainfall (mm)")
        plt.grid()
        plt.savefig(appfolder+'static/charts'
                            '/'+stationName+'_6month.png')
        plt.close()
        # Spi12 and Rdi12 Chart-------------------------------------------------------------------------------------------
        Spi12= spiresults["Spi12"]['Spi_result']
        Rdi12= rdiresults["Rdi12"]['Rdi_result']
        plt.figure(figsize=(6*3.13,4*3.13))
        plt.subplot(211)
        n=len(Spi12)
        ind = np.arange(n)
        width = 0.40
        plt.axhspan(0, -0.8, facecolor='0.5', alpha=0.5,color ='yellow',linewidth = True)
        plt.axhspan(-0.8, -1.3, facecolor='0.5', alpha=0.5,color ='orange',linewidth = True)
        plt.axhspan(-1.3, -1.6, facecolor='0.5', alpha=0.5,color ='orangered',linewidth = True)
        plt.axhspan(-1.6, -2, facecolor='0.5', alpha=0.5,color ='r',linewidth = True)
        plt.axhspan(-2, -3, facecolor='0.5', alpha=0.5,color ='maroon',linewidth = True)
        rects1 = plt.bar(ind, Spi12, width, color='b', label='Spi ')
        rects2 = plt.bar(ind + width, Rdi12, width, color='lightblue', label='Rdi ')
        plt.ylabel('Drought Index - std units')
        plt.title('{} {} Drought Propagation Chart for The Period {} - {}'.format('[12 Month]', stationname,minyear,maxyear))
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
        plt.scatter(Spi12,rain12_data,label='SPI ')
        plt.scatter(Rdi12,rain12_data,c="lightblue",label='RDI')
        plt.legend(bbox_to_anchor=(1.025, 1), loc=2, borderaxespad=0.)
        plt.xlabel("Drought Index")
        plt.ylabel("Rainfall (mm)")
        plt.grid()
        plt.savefig(appfolder+'static/charts'
                            '/'+stationName+'_12month.png')
        plt.close()
        print stationName, "Charts Update run completed... OK"
    except Exception, e:
        print "Drought Error for", stationName,":", e.message, e.args
