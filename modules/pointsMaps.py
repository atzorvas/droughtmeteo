#-------------------------------------------------------------------------------
# Name:        	Point maps
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
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import re
from gluon import current
import Image
import datetime
import calendar
#Create list weather stations points/  point shapefile with the location of Weather Stations

def prepareString(str):
    str = str.split(" ")
    str[2] = str[2][:1]+".00"+str[2][2]
    str = ''.join(str)
    return str


def dms2dec(dms_str):
    dms_str = prepareString(dms_str)
    dms_str = re.sub(r'\s', '', dms_str)
    if re.match('[swSW]', dms_str):
        sign = -1
    else:
        sign = 1

    (degree, minute, second, frac_seconds, junk) = re.split('\D+', dms_str, maxsplit=4)
    return sign * (int(degree) + float(minute) / 60 + float(second) / 3600 + float(frac_seconds) / 36000)


def run(appfolder, stationNames, stationLocations, spiValues):
    print "Maps::", appfolder, stationNames, stationLocations, spiValues
    SpiValuefromCurrentdroughtpy = spiValues
    print SpiValuefromCurrentdroughtpy
    StationsLocation = stationLocations
    for loc in StationsLocation:
        loc[0] = dms2dec(loc[0])
        loc[1] = dms2dec(loc[1])
    fig = plt.figure(figsize=(7*3.13,5*3.13))
    map = Basemap(projection='merc', lat_0=57, lon_0=-135,
        resolution = 'h', area_thresh = 0.1,
        llcrnrlon=18, llcrnrlat=34,
        urcrnrlon=35, urcrnrlat=45)
    print "start to draw..."
    map.drawcoastlines()
    map.drawcountries()
    #map.fillcontinents(color='coral')
    map.drawmapboundary()
    map.drawmeridians(np.arange(0, 360, 30))
    map.drawparallels(np.arange(-90, 90, 30))
    map.bluemarble()
    #map.drawmapscale()
    print "draw point 2"
    lon =[]
    lat =[]
    colour=[]
    xall = []
    yall = []

    for i,spival  in zip(range(0,len(StationsLocation)),SpiValuefromCurrentdroughtpy):
        if -0.7 <= np.float64(spival) <= 0:
            colourin = 'yellow'
        elif -1.2 <= np.float64(spival) <= -0.8:
            colourin = 'orange'
        elif -1.5 <= np.float64(spival) <= -1.3:
            colourin = 'orangered'
        elif -1.9 <= np.float64(spival) <= -1.6:
            colourin = 'r'
        elif -2 >= np.float64(spival):
            colourin = 'maroon'
        elif np.float64(spival) > 0:
            colourin = 'b'
        colour.append(colourin)
        lon.append(StationsLocation[i][1])
        lat.append(StationsLocation[i][0])
        x,y=map(StationsLocation[i][1], StationsLocation[i][0])
        xall.append(x)
        yall.append(y)
        map.plot(x,y,'o', color=colourin,markersize=6)
    print "draw point 3"
    x_offsets = [10000, 30000, 25000]
    y_offsets = [5000, 25000, 25000]
    for  xpt, ypt, spival in zip( xall, yall, SpiValuefromCurrentdroughtpy):
        print  '%.2f' % np.float64(spival)
        colourin = ''
        if -0.7 <= np.float64(spival) <= 0:
            message = "D0"
            colourin = 'yellow'
        elif -1.2 <= np.float64(spival) <= -0.8:
            message = "D1"
            colourin = 'orange'
        elif -1.5 <= np.float64(spival) <= -1.3:
            message = "D2"
            colourin = 'orangered'
        elif -1.9 <= np.float64(spival) <= -1.6:
            message = "D3"
            colourin = 'r'
        elif -2 >= np.float64(spival):
            message = "D4"
            colourin = 'maroon'
        elif np.float64(spival) > 0:
            message = "W"
            colourin = 'b'
        plt.text(xpt +5000, ypt + 5000, message, color=colourin)
    print "end map!!"
    print current.request.folder+'/static/images/legendMap.png'
    print "end end.."
    im = Image.open(current.request.folder+'/static/images/legendMap.png')
    height = im.size[1]
    im = np.array(im).astype(np.float) / 255
    fig.figimage(im,xo=1870, yo=160,origin='upper')
    im2 = Image.open(current.request.folder+'/static/images/logo.jpg')
    height = im2.size[1]
    fig.figimage(im2,xo=150, yo=160,origin='upper')
    # We need a float array between 0-1, rather than
    # a uint8 array between 0-255
    im = np.array(im).astype(np.float) / 255
    plt.grid()
    plt.title("Meteo.gr Drought Station Network "+calendar.month_name[datetime.datetime.now().month]+ " " + str(datetime.datetime.now().year))
    plt.savefig(appfolder + '/static/images/stations.png')
    return "YEAH!"
