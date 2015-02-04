#-------------------------------------------------------------------------------
# Name:        	Current Drought Conditions
# Purpose:     	Drought live Greece Monitor
#
# Author:      	Anastasiadis Stavros / Antonis Tsorvas
#
# Created:     	13/09/2013
# Copyright:   	(c) Anastasiadis Stavros 2013
#              	(c) Tzorvas Konstantinos Antonis 2013
# Licence:     	MIT
#-------------------------------------------------------------------------------
import datetime
import scipy.stats as ss
import numpy as np


def spi_calc(spi_input_data):
    #SPI general Calculation function
    print 'spi-calc 1'
    fit_k, fit_loc, fit_theta = ss.gamma.fit(spi_input_data)
    print 'spi-calc 2'
    data_cdf = ss.gamma.cdf(spi_input_data, fit_k, fit_loc, fit_theta)
    print 'spi-calc 3'
    data_SPI = ss.zscore(data_cdf)
    print 'spi-calc 4'
    return dict(fit_k=fit_k, fit_theta=fit_theta, Spi_result=data_SPI)


def run(stationName, data):
    Data = data
    Station_Name = stationName
    for k, v in data.iteritems():
        Data[int(k)] = {}
        for a, b in v.iteritems():
            Data[int(k)][int(a)] = map(lambda x: x if x != None else 0, b)

    # Current Drought
    now = datetime.datetime.now()
    month = now.month
    Years = Data.keys()
    print "run -----------drought"

    datamonth = []
    for Year in Years:
        print "calc", Data[Year][month][0]
        datamonth.append(Data[Year][month][0])
    print "calling spi_calc for:", datamonth
    a = spi_calc(datamonth)

    print "run 2 ---- drought"
    SpiValue = a['Spi_result'].mean()
    #classification http://droughtmonitor.unl.edu/classify.htm
    if -0.7 <= SpiValue <= 0:
        message = "Abnormally Dry - D0"
    elif -1.2 <= SpiValue <= -0.8:
        message = "Moderate Dry - D1"
    elif -1.5 <= SpiValue <= -1.3:
        message = "Severe Drought Dry - D2"
    elif -1.9 <= SpiValue <= -1.6:
        message = "Extreme Dry - D3"
    elif -2 >= SpiValue:
        message = "Exceptional Dry - D4"
    elif SpiValue > 0:
        message = "Wet Conditions"
    print "!!", SpiValue, a
    current = dict(station=Station_Name, value=message, spivalue=SpiValue)
    print "done with currentDrought!"
    return current
    # Current - Prepei na apothikeuei to Message kathe 1 tou mina opws ta grafimata se ena table
    # Sto Home tha yparxei, pinakas me sthles (Station  , Drought Conditions)
    # Katw apo ton pinaka tha prosthesw sxolia

    # Me alla logia, kathe fora pou tha trexei auto to scpirt, gia kathe sta8mo tha apothikeyei thn
    # metabliti Current se Pinaka px CurrentDroughts kai sto Home tha dinei ta results
