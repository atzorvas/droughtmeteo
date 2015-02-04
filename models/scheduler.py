from gluon.scheduler import Scheduler
from gluon import current

def clearUserCharts():
    import time
    newLine = "Your new line of data with the time stamp goes here.\n"
    for item in db(db.userfiles).select():
        res = float(item.time) <= time.time()
        newLine += "time generated SMALLER or EQUAL" if res else "time generated BIGGER"
        newLine += "\n" + item.time + " - " + str(time.time())


def updateCharts():
    import actions
    import os
    actions.delCharts(os, current.request.folder) #first delete all charts
    try:
        for station in db(db.stations).select():
            import DroughtAlgo
            DroughtAlgo.run(current.request.folder+"/", '_'.join(station.name.split()), actions.getData(db,station.id))
        return "success"
    except Exception, e:
        return "fail", e


def updateMap():
    updateCurrent() #call first
    stationNames = []
    stationLocations = []
    spiValues = []
    try:
        for station, current in zip(db(db.stations).select(), db(db.current).select()):
            stationNames.append(station.name)
            stationLocations.append([station.lat, station.long])
            spiValues.append(current.spivalue)
    except Exception, e:
        return "fail"

    try:
        import pointsMaps
        from gluon import current
        pointsMaps.run(current.request.folder, stationNames, stationLocations, spiValues)
        return "success"
    except Exception,e:
        return "failed", e, e.args, e.message, e.__class__


def insertCurrent(db,data):
    try:
        db.current.insert(station_id = data['station'],
                          value = data['value'],
                          spivalue = data['spivalue'])
        db.commit()
        return "success"
    except:
        return "fail"


def updateCurrent():
    try:
        db.current.truncate()
        for station in db(db.stations).select():
            import CurrentDrought, actions
            insertCurrent(db, CurrentDrought.run(station.id, actions.getData(db, station.id)))
        return "success"
    except Exception, e:
        return "fail"


scheduler = Scheduler(db, dict(updateCharts=updateCharts, updateMaps=updateMap, clearUserCharts=clearUserCharts))
