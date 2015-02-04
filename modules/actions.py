import ast
import DroughtAlgo
import pointsMaps
import CurrentDrought
import requests

def isnoaurl(url):
    if (url.startswith("http://penteli.meteo.gr/meteosearch/data/")) and (url.endswith('.txt')) and requests.get(url).status_code == 200:
        return True
    else:
        return False

def temppopulate(db, session, redirect, URL):
    records = db.temp_noadata(db.temp_noadata.station_id == session.lastid) or None
    this_station = db.stations(db.stations.id == session.lastid) or redirect(URL('index'))
    if records==None:
        myList = []
        for record in this_station.temp_data_list:
            print "record", record
            myList.append(ast.literal_eval(record))
        for record in myList:
            print "RECORD:", record
            db.temp_noadata.insert(station_id=this_station.id, year=record.get('year'),
                                   jan=record.get('jan'),
                                   feb=record.get('feb'),
                                   mar=record.get('mar'),
                                   apr=record.get('apr'),
                                   may=record.get('may'),
                                   jun=record.get('jun'),
                                   jul=record.get('jul'),
                                   aug=record.get('aug'),
                                   sep=record.get('sep'),
                                   oct=record.get('oct'),
                                   nov=record.get('nov'),
                                   dec=record.get('dec'))
        print "End with temppopulate"
    else:
        print "Already Filled!"

def populate(db, session, redirect, URL):
    records = db.noadata(db.noadata.station_id == session.lastid) or None
    this_station = db.stations(db.stations.id == session.lastid) or redirect(URL('index'))
    if records==None:
        myList = []
        for record in this_station.data_list:
            myList.append(ast.literal_eval(record))
        for record in myList:
            print "rain RECORD:: ", record
            db.noadata.insert(station_id=this_station.id, year=record.get('year'),
                                   jan=record.get('jan'),
                                   feb=record.get('feb'),
                                   mar=record.get('mar'),
                                   apr=record.get('apr'),
                                   may=record.get('may'),
                                   jun=record.get('jun'),
                                   jul=record.get('jul'),
                                   aug=record.get('aug'),
                                   sep=record.get('sep'),
                                   oct=record.get('oct'),
                                   nov=record.get('nov'),
                                   dec=record.get('dec'))
        temppopulate(db, session, redirect, URL)
    else:
        print "Already Filled!"

def updateRain(db, session, stationid, data):
    rain = data['RAIN']
    for pos, raind in enumerate(rain):
        rec_year = rain[pos]
        if len(db((db.noadata.station_id==stationid)&(db.noadata.year==raind['year'])).select()) == 0:
            db.noadata.insert(station_id=stationid, year=rec_year.get('year'),
                               jan=rec_year.get('jan'),
                               feb=rec_year.get('feb'),
                               mar=rec_year.get('mar'),
                               apr=rec_year.get('apr'),
                               may=rec_year.get('may'),
                               jun=rec_year.get('jun'),
                               jul=rec_year.get('jul'),
                               aug=rec_year.get('aug'),
                               sep=rec_year.get('sep'),
                               oct=rec_year.get('oct'),
                               nov=rec_year.get('nov'),
                               dec=rec_year.get('dec'))
        else:
            for k,v in rec_year.iteritems():
                if k!="year" and db((db.noadata.station_id==stationid) & (db.noadata.year==raind['year'])).select()[0][k] == None:
                    db((db.noadata.station_id==stationid) & (db.noadata.year==rec_year['year'])).update(**{k: v})#.select()[0][k]
    print "exit..."

def updateTemp(db, session, stationid, data):
    temp = data['TEMP']
    for pos, tempd in enumerate(temp):
        rec_year = temp[pos]
        if len(db((db.temp_noadata.station_id==stationid)&(db.temp_noadata.year==tempd['year'])).select()) == 0:
            db.temp_noadata.insert(station_id=stationid, year=rec_year.get('year'),
                               jan=rec_year.get('jan'),
                               feb=rec_year.get('feb'),
                               mar=rec_year.get('mar'),
                               apr=rec_year.get('apr'),
                               may=rec_year.get('may'),
                               jun=rec_year.get('jun'),
                               jul=rec_year.get('jul'),
                               aug=rec_year.get('aug'),
                               sep=rec_year.get('sep'),
                               oct=rec_year.get('oct'),
                               nov=rec_year.get('nov'),
                               dec=rec_year.get('dec'))
        else:
            for k,v in rec_year.iteritems():
                if k!="year" and db((db.temp_noadata.station_id==stationid) & (db.temp_noadata.year==tempd['year'])).select()[0][k] == None:
                    db((db.temp_noadata.station_id==stationid) & (db.temp_noadata.year==rec_year['year'])).update(**{k: v})#.select()[0][k]
    print "exit..."

def read_file(db, session, redirect, URL, request, os, recordid):
    records = db.emydata(db.emydata.station_id == recordid) or None
    this_station = db.stations(db.stations.id == recordid) or redirect(URL('index'))
    print "Changing station:", this_station.name
    print "read file 1"
    print records
    if records == None:
        txt = os.path.join(request.folder, "uploads", this_station.emy_file)
        file = open(txt, 'r')
        data = filter(None, file.read().split("\n")[1:])
        print "read file 2"
        for record in data:
            record = record.split(",")
            rec_year = {"year": record[0], "jan": record[1], "feb": record[2], "mar": record[3],
                        "apr": record[4], "may": record[5], "jun": record[6], "jul": record[7],
                        "aug": record[8], "sep": record[9], "oct": record[10], "nov": record[11], "dec": record[12]}

            #print "Read File: ", rec_year
            db.emydata.insert(station_id=this_station.id, year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))
            try:
                temp_year = {"year": record[13], "jan": record[14], "feb": record[15], "mar": record[16],
                            "apr": record[17], "may": record[18], "jun": record[19], "jul": record[20],
                            "aug": record[21], "sep": record[22], "oct": record[23], "nov": record[24], "dec": record[25]}
                db.temp_emydata.insert(station_id=this_station.id, year=temp_year.get('year'),
                                           jan=temp_year.get('jan'),
                                           feb=temp_year.get('feb'),
                                           mar=temp_year.get('mar'),
                                           apr=temp_year.get('apr'),
                                           may=temp_year.get('may'),
                                           jun=temp_year.get('jun'),
                                           jul=temp_year.get('jul'),
                                           aug=temp_year.get('aug'),
                                           sep=temp_year.get('sep'),
                                           oct=temp_year.get('oct'),
                                           nov=temp_year.get('nov'),
                                           dec=temp_year.get('dec'))
            except:
                print ""
        print "read file 3"
    else:
        return "EMYDB Already filled with Values! for station:", this_station.name

def calc_data(db, session, redirect, URL, request):
    def merge_rows(row1, row2):
        #row1 emydata
        #row2 noadata
        row3 = row1.copy()
        months = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
        sum = 0
        for i in range(0,len(months)):
            if row2[months[i]]:
                row3[months[i]] = row2[months[i]]
            else:
                row3[months[i]] = row1[months[i]]
            sum += row3[months[i]]
        return row3
    print "hi"
    for station in db(db.stations).select():
        db(db.alldata.station_id==station.id).delete()
        noa = db(db.noadata.station_id==station.id).select(orderby=db.noadata.year)
        emy = db(db.emydata.station_id==station.id).select(orderby=db.emydata.year)

        if len(noa) == 0:
            equery = (db.emydata.station_id==station.id)
            rec_year = db(equery).select()
            for rec_year in rec_year:
                #print rec_year['jan']
                #for key,value in rec_year.iteritems():
                #    rec_year=value
                #    #print key,value
                db.alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))

        elif len(emy) == 0:
            nquery = (db.noadata.station_id==station.id)
            rec_year = db(nquery).select().as_dict()
            for key,value in rec_year.iteritems():
                rec_year=value
                db.alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))

        else:
            emy_max = emy.last()['year']
            emy_min = emy.first()['year']
            noa_min = noa.first()['year']
            noa_max = noa.last()['year']
            if emy_max < noa_min:
                for year in range(emy_min,emy_max+1): #rest years
                    nquery = (db.emydata.year==year) & (db.emydata.station_id==station.id)
                    rec_year = db(nquery).select()[0].as_dict()
                    db.alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))
                for year in range(noa_min,noa_max+1):
                    nquery = (db.noadata.year==year) & (db.noadata.station_id==station.id)
                    rec_year = db(nquery).select()[0].as_dict()
                    db.alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))
            else:
                for year in range(noa_min,emy_max+1): #years in conflict
                    equery = (db.emydata.year==year) & (db.emydata.station_id==station.id)
                    nquery = (db.noadata.year==year) & (db.noadata.station_id==station.id)
                    aquery = (db.alldata.year==year) & (db.alldata.station_id==station.id)
                    rec_year = merge_rows(db(equery).select()[0].as_dict(), db(nquery).select()[0].as_dict())

                    db.alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))
                for year in range(emy_min,noa_min): #rest years
                    nquery = (db.emydata.year==year) & (db.emydata.station_id==station.id)
                    rec_year = db(nquery).select()[0].as_dict()
                    db.alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))
                for year in range(emy_max+1,noa_max+1): #rest years
                    nquery = (db.noadata.year==year) & (db.noadata.station_id==station.id)
                    rec_year = db(nquery).select()[0].as_dict()
                    db.alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))
    print "Success"
    temp_calc_data(db, session, redirect, URL, request)

def temp_calc_data(db, session, redirect, URL, request):
    def merge_rows(row1, row2):
        #row1 emydata
        #row2 noadata
        row3 = row1.copy()
        months = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
        sum = 0
        for i in range(0,len(months)):
            if row2[months[i]]:
                row3[months[i]] = row2[months[i]]
            else:
                row3[months[i]] = row1[months[i]]
            sum += row3[months[i]]
        return row3

    for station in db(db.stations).select():
        db(db.temp_alldata.station_id==station.id).delete()
        noa = db(db.temp_noadata.station_id==station.id).select(orderby=db.temp_noadata.year)
        emy = db(db.temp_emydata.station_id==station.id).select(orderby=db.temp_emydata.year)

        if len(noa) == 0:
            equery = (db.temp_emydata.station_id==station.id)
            rec_year = db(equery).select()
            for rec_year in rec_year:
                #print rec_year['jan']
                #for key,value in rec_year.iteritems():
                #    rec_year=value
                #    #print key,value
                db.temp_alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))

        elif len(emy) == 0:
            nquery = (db.temp_noadata.station_id==station.id)
            rec_year = db(nquery).select().as_dict()
            for key,value in rec_year.iteritems():
                rec_year=value
                db.temp_alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))

        else:
            emy_max = emy.last()['year']
            emy_min = emy.first()['year']
            noa_min = noa.first()['year']
            noa_max = noa.last()['year']

            if emy_max < noa_min:
                for year in range(emy_min,emy_max+1): #rest years
                    nquery = (db.temp_emydata.year==year) & (db.temp_emydata.station_id==station.id)
                    rec_year = db(nquery).select()[0].as_dict()

                    db.temp_alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))
                for year in range(noa_min, noa_max+1):
                    nquery = (db.temp_noadata.year==year) & (db.temp_noadata.station_id==station.id)
                    rec_year = db(nquery).select()[0].as_dict()
                    db.temp_alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))

            else:
                for year in range(noa_min,emy_max+1): #years in conflict
                    print "years conflick", year
                    equery = (db.temp_emydata.year==year) & (db.temp_emydata.station_id==station.id)
                    nquery = (db.temp_noadata.year==year) & (db.temp_noadata.station_id==station.id)
                    aquery = (db.temp_alldata.year==year) & (db.temp_alldata.station_id==station.id)
                    rec_year = merge_rows(db(equery).select()[0].as_dict(), db(nquery).select()[0].as_dict())

                    db.temp_alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))
                for year in range(emy_min,noa_min): #rest years
                    print "years emy rest", year
                    nquery = (db.temp_emydata.year==year) & (db.temp_emydata.station_id==station.id)
                    rec_year = db(nquery).select()[0].as_dict()
                    db.temp_alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))

                for year in range(noa_min,noa_max): #rest years
                    print "years noa rest", year
                    nquery = (db.temp_noadata.year==year) & (db.temp_noadata.station_id==station.id)
                    rec_year = db(nquery).select()[0].as_dict()
                    db((db.temp_alldata.year == rec_year['year'])&(db.temp_alldata.station_id == rec_year['station_id'])).delete()
                    db.temp_alldata.insert(station_id=rec_year.get('station_id'), year=rec_year.get('year'),
                                       jan=rec_year.get('jan'),
                                       feb=rec_year.get('feb'),
                                       mar=rec_year.get('mar'),
                                       apr=rec_year.get('apr'),
                                       may=rec_year.get('may'),
                                       jun=rec_year.get('jun'),
                                       jul=rec_year.get('jul'),
                                       aug=rec_year.get('aug'),
                                       sep=rec_year.get('sep'),
                                       oct=rec_year.get('oct'),
                                       nov=rec_year.get('nov'),
                                       dec=rec_year.get('dec'))
    print "Success"

def getData(db, id):
    try:
        labels = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        if id:
            rain = db(db.alldata.station_id==id).select()
            temp = db(db.temp_alldata.station_id==id).select()
            results = {}
            r = db(db.alldata).select(db.alldata.year, orderby=db.alldata.year)
            first = int(r.first()['year'])
            last = int(r.last()['year'])
            for a in rain:
                rain = {'1': [a.as_dict()['jan'], None],
                            '2': [a.as_dict()['feb'], None],
                            '3': [a.as_dict()['mar'], None],
                            '4': [a.as_dict()['apr'], None],
                            '5': [a.as_dict()['may'], None],
                            '6': [a.as_dict()['jun'], None],
                            '7': [a.as_dict()['jul'], None],
                            '8': [a.as_dict()['aug'], None],
                            '9': [a.as_dict()['sep'], None],
                            '10': [a.as_dict()['oct'], None],
                            '11': [a.as_dict()['nov'], None],
                            '12': [a.as_dict()['dec'], None],
                            }
                results[int(a.year)] = rain
            for b in temp:
                results[int(b.year)]['1'][1] = b.as_dict()['jan']
                results[int(b.year)]['2'][1] = b.as_dict()['feb']
                results[int(b.year)]['3'][1] = b.as_dict()['mar']
                results[int(b.year)]['4'][1] = b.as_dict()['apr']
                results[int(b.year)]['5'][1] = b.as_dict()['may']
                results[int(b.year)]['6'][1] = b.as_dict()['jun']
                results[int(b.year)]['7'][1] = b.as_dict()['jul']
                results[int(b.year)]['8'][1] = b.as_dict()['aug']
                results[int(b.year)]['9'][1] = b.as_dict()['sep']
                results[int(b.year)]['10'][1] = b.as_dict()['oct']
                results[int(b.year)]['11'][1] = b.as_dict()['nov']
                results[int(b.year)]['12'][1] = b.as_dict()['dec']
        else:
            results = None
        #print "1966", results[1960]
    except Exception,e:
        print e.message
    return results or None

def getData2(db, id):
    labels = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    if id:
        rain = db(db.noadata.station_id==id).select()
        temp = db(db.temp_noadata.station_id==id).select()
        results = {}
        for a,b in zip(rain,temp):
            rain = {'1': [a.as_dict()['jan'], b.as_dict()['jan']],
                    '2': [a.as_dict()['feb'], b.as_dict()['feb']],
                    '3': [a.as_dict()['mar'], b.as_dict()['mar']],
                    '4': [a.as_dict()['apr'], b.as_dict()['apr']],
                    '5': [a.as_dict()['may'], b.as_dict()['may']],
                    '6': [a.as_dict()['jun'], b.as_dict()['jun']],
                    '7': [a.as_dict()['jul'], b.as_dict()['jul']],
                    '8': [a.as_dict()['aug'], b.as_dict()['aug']],
                    '9': [a.as_dict()['sep'], b.as_dict()['sep']],
                    '10': [a.as_dict()['oct'], b.as_dict()['oct']],
                    '11': [a.as_dict()['nov'], b.as_dict()['nov']],
                    '12': [a.as_dict()['dec'], b.as_dict()['dec']],
                    }
            results[a.year] = rain
    else:
        results = None
    return results

def delCharts(os, appfolder):
    print "del charts.. ", appfolder
    for root, dirs, files in os.walk(appfolder+'/static/charts'):
        for f in files:
            os.unlink(os.path.join(root, f))
        return "success"


def delStationCharts(os, appfolder, station):
    print "will delete...", station
    for root, dirs, files in os.walk(appfolder+'/static/charts'):
        for f in files:
            if f.startswith(station+"_") and f.endswith(".png"):
                os.unlink(os.path.join(root, f))
        return "success"

def updateGraphs(os, db, appfolder):
    print "into action.."
    delCharts(os, appfolder) #first delete all charts
    try:
        for station in db(db.stations).select():
            #getData(db,station.id)
            DroughtAlgo.run(appfolder, '_'.join(station.name.split()), getData(db,station.id))
            print "after"
        return "success"
    except Exception, e:
        return "fail", e

def updateMap(os, db, appfolder):
    stationNames = []
    stationLocations = []
    spiValues = []
    print "updateMap"
    try:
        for station, current in zip(db(db.stations).select(), db(db.current).select()):
            stationNames.append(station.name)
            stationLocations.append([station.lat, station.long])
            spiValues.append(current.spivalue)
    except Exception, e:
        return "fail"

    try:
        #print "---", pointsMaps.dms2dec(stationLocations[0][0])
        #pointsMaps.run(appfolder, stationNames, stationLocations, spiValues)r
        pointsMaps.run(appfolder, stationNames, stationLocations, spiValues)
        return "success"
    except:
        return "failed"

def insertCurrent(db,data):
    print "---Insert Current"
    try:
        db.current.insert(station_name = data['station'],
                          value = data['value'],
                          spivalue = data['spivalue'])
        print "---Insert Current --- OK"
        return "success"
    except:
        print "---Insert Current --- FAIL"
        return "fail"

def updateCurrent(db):
    counter = 0
    try:
        db.current.truncate()
        for station in db(db.stations).select():
            insertCurrent(db, CurrentDrought.run(station.name, getData(db, station.id)))
            counter += 1
        return "success"
    except Exception, e:
        return "fail"
