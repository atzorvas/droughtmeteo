# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()

import time
### end requires


def index():
    redirect(URL('default', 'index'))

@auth.requires_membership('admin')
def add():
    session.msg = ''
    form = SQLFORM.factory(Field('url', requires=IS_NOT_EMPTY())
                           #Field('extra_ases', 'boolean'),
                           #Field('extra_emy', 'boolean'),
                           #Field('ASES', 'upload', uploadfolder="./"),
                           #Field('EMY', 'upload', uploadfolder="./")
    )
    form.add_button('Back to Admin Page', URL('admin', 'panel'))
    #print form. form[0][1]
    #form.element('#no_table_ASES__row')['_style']="display:none;"
    #form.element('#no_table_EMY__row')['_style']="display:none;"
    #form.element('#no_table_extra_ases')['_onchange'] = "if(jQuery('#no_table_extra_ases').prop('checked')) jQuery('#no_table_ASES__row').show(); else jQuery('#no_table_ASES__row').hide();"
    #form.element('#no_table_extra_emy')['_onchange'] = "if(jQuery('#no_table_extra_emy').prop('checked')) jQuery('#no_table_EMY__row').show(); else jQuery('#no_table_EMY__row').hide();"
    if form.accepts(request.vars, session):
        print "accepted"
        from actions import isnoaurl
        if isnoaurl(form.vars.url):
            print "ok"
            import noainfo
            mystation = noainfo.station(form.vars.pop('url'))
            session.tmpstation = mystation
            session.laststation = time.time()
            session.confirm = 1
            redirect(URL('confirm.html'), client_side=True)
            #response.js = "window.open('"+ URL('stations', 'confirm.html') +"', '_blank', 'toolbar=0,location=0,menubar=0,width=800,height=560');"
        else:
            print "ok"
            response.flash = T('Please enter a valid url')
            form.errors.url = 'please enter a valid url'

    if form.process().accepted:
        print "here"
        from actions import isnoaurl
        if isnoaurl(form.vars.url):
            print "ok"
            import noainfo
            mystation = noainfo.station(form.vars.pop('url'))
            session.tmpstation = mystation
            session.laststation = time.time()
            session.confirm = 1
            redirect(URL('confirm'))
        else:
            print "ok"
            response.flash = T('Please enter a valid url')
            form.errors.url = 'please enter a valid url'
    return dict(form=form)

@auth.requires_membership('admin')
def confirm():
    print db.stations.name.length
    TIMEOUT=60*2
    button = BUTTON("go back!", _onclick='history.back()')
    if session.tmpstation:
        if not session.laststation<time.time()-TIMEOUT:
            print vars(session.tmpstation)['_data']
            db.stations.emy_file.writable = db.stations.emy_file.readable = False
            db.stations.noa_url.default = vars(session.tmpstation)['_info'].get('urlbase')
            db.stations.noa_url.writable = False
            db.stations.name.default = vars(session.tmpstation)['_info'].get('NAME')
            #db.stations.name.writable = False
            db.stations.city.default = vars(session.tmpstation)['_info'].get('CITY')
            #db.stations.city.writable = False
            db.stations.state.default = vars(session.tmpstation)['_info'].get('STATE')
            #db.stations.state.writable = False
            db.stations.lat.default = vars(session.tmpstation)['_info'].get('LAT')
            #db.stations.lat.writable = False
            db.stations.long.default = vars(session.tmpstation)['_info'].get('LONG')
            #db.stations.long.writable = False
            db.stations.elev.default = vars(session.tmpstation)['_info'].get('ELEV')
            #db.stations.elev.writable = False
            db.stations.data_from.default = vars(session.tmpstation)['_info'].get('from')
            db.stations.data_from.writable = False
            db.stations.data_to.default = vars(session.tmpstation)['_info'].get('to')
            db.stations.data_to.writable = False
            db.stations.data_list.default = vars(session.tmpstation)['_data'].get('RAIN')
            db.stations.data_list.writable = False
            db.stations.data_list.readable = False
            db.stations.temp_data_list.default = vars(session.tmpstation)['_data'].get('TEMP')
            db.stations.temp_data_list.writable = False
            db.stations.temp_data_list.readable = False
            db.stations.noa_url.requires = IS_NOT_IN_DB(db, 'stations.noa_url')
        else: # delete vars...
            del session.tmpstation
            del session.laststation
            redirect(URL('add')) #go back to add
    else:
        redirect(URL('add'))
    print db.stations.name.length
    form = SQLFORM(db.stations)
    form.element(_type='submit')['_onclick'] = "msg=''"
    script=SCRIPT("setTimeout(function(){var msg='Form will be erased and you will be prompted at add page';window.onbeforeunload = function() "
                  "{if (msg!='') {return msg;}};},"+str(TIMEOUT*1000+session.laststation*1000-int(time.time()*1000))+");")

    if form.process().accepted:
        print "ohai"
        import actions
        session.lastid = form.vars.id
        actions.populate(db, session, redirect, URL)
        actions.calc_data(db, session, redirect, URL, request)
        session.flash = T('Station ' + form.vars.name + ' created!')
        redirect(URL('stations', 'add'))
    elif form.errors:
        print "ohoi"
        response.flash = T('Failed')
    return dict(form=form+script, button=button)

@auth.requires_membership('admin')
def show():
    session.flash = ''
    print request.vars.station
    print request.args(0)
    form = SQLFORM.factory(Field('station', requires=IS_IN_DB(db, db.stations.id,'%(name)s'),
                                 default=request.vars.station or request.args(0)),
                           Field('var', requires=IS_IN_SET(['Rainfall', 'Temp']), default=request.vars.var,
                                 readable=True if request.vars.station else False, writable=True if request.vars.station else False))
    form.element(_id="no_table_station")['_onchange'] = "this.form.submit();"
    results = ''
    info = ''
    if request.vars.station:
        this_station = db.stations(db.stations.id == request.vars.station)
        if request.vars.var == 'Rainfall':
            data = db(db.alldata.station_id == this_station.id).select()
        else:
            data = db(db.temp_alldata.station_id == this_station.id).select()
        info = TABLE(TR(TD('Name:'),TD(this_station['name']), TD(''), TD(''), TD('City:'),TD(this_station['city']), TD(''), TD(''), TD('State:'),TD(this_station['state'])),
                      TR(TD('Elev'),TD(this_station['elev']), TD(''), TD(''), TD('Lang:'),TD(this_station['long'], TD(''), TD(''), TD('Lat:'), TD(this_station['lat']))),)
        results = TABLE(TR(TH('Year'),TH('Jan'), TH('Feb'), TH('Mar'), TH('Apr'), TH('May'), TH('Jun'), TH('Jul'), TH('Aug'), TH('Sep'), TH('Oct'), TH('Nov'), TH('Dec')), [TR(TD(record['year']), TD(record['jan']), TD(record['feb']), TD(record['mar']), TD(record['apr']), TD(record['may']), TD(record['jun']), TD(record['jul']), TD(record['aug']), TD(record['sep']), TD(record['oct']), TD(record['nov']), TD(record['dec'])) for record in data])
    return dict(form=form, info=info, results=results)


@auth.requires_membership('admin')
def edit():
    this_station = db.stations(db.stations.id==request.args(0))
    if request.args:
        db.stations.data_list.writable = db.stations.temp_data_list.writable = False
        db.stations.data_list.readable = db.stations.temp_data_list.readable = False
        #db.stations.data_from.writable = db.stations.data_to.writable = False

        form = crud.update(db.stations, this_station.id)#, onaccept=)
        if form.accepted:
            import actions, os
            if form.vars.delete_this_record=='on':
                import os
                actions.delStationCharts(os, request.folder, this_station.name)
            elif form.vars.emy_file != None and form.vars.emy_file != '':
                db(db.emydata.station_id==form.record_id).delete()
                db(db.temp_emydata.station_id==form.record_id).delete()
                db(db.alldata.station_id==form.record_id).delete()
                db(db.temp_alldata.station_id==form.record_id).delete()
                actions.read_file(db, session, redirect, URL, request, os, form.record_id)
                actions.calc_data(db, session, redirect, URL, request)
    else:
        form = SQLFORM.factory(Field('station', requires=IS_IN_DB(db, db.stations.name, '%(name)s')))
        if form.process().accepted:
            this_station = db.stations(db.stations.name==request.vars.station)
            redirect(URL('stations', 'edit', args=this_station.id))
    return dict(form=form)


@auth.requires_login()
def charts():
    session.forget(response)
    chart = ''
    if request.vars.station:
        requires = IS_IN_SET(['1 month', '3 month', '6 month', '12 month'])
    else:
        requires = IS_IN_SET([])

    if request.vars.station != None and request.vars.chart != '':
        url = URL('static', 'charts', args='_'.join(request.vars.station.split()) + '_' + ''.join(request.vars.chart.split()) +'.png')
        chart = IMG(_src=url, width=500, height=500)

    form = SQLFORM.factory(Field('station', requires=IS_IN_DB(db, 'stations.name'), default=request.vars.station),#writable=False if request.args(0)!=None else True),
                           Field('chart', requires=requires,default=request.vars.chart, label="Select Time Span", required=False))
    form.element(_id="no_table_station__label")['_style'] = "font-weight:bold;"
    form.element(_id="no_table_chart__label")['_style'] = "font-weight:bold;"
    form.element(_id="no_table_station")['_onchange'] = "jQuery('#no_table_chart').val('');this.form.submit()"
    return dict(form=form, chart=chart)


@auth.requires_login()
def userAdd():
    import useractions, os
    data = False
    station = None
    res = db.userfiles(db.userfiles.owner==auth.user.id)
    form = SQLFORM(db.userfiles)

    if (res is not None) and (float(res.time) <= time.time()):
        print "deleting old data.."
        db(db.userfiles.owner == auth.user.id).delete()
        useractions.delUserCharts(os, request.folder+"/", auth.user.id)
        station = ''
    elif res is None:
        print "no data to show.."
        data = False
    else:
        print "has data to show!"
        data = True
        station = res.station_name
    if form.process().accepted:
        import UserSPI
        db(db.userfiles.owner == auth.user.id).delete()
        useractions.delUserCharts(os, request.folder+"/", auth.user.id)
        response.flash = 'form accepted'
        data = useractions.read_file_user(db, form.vars.id, request.folder, os)
        UserSPI.run(request.folder, '_'.join(request.vars.station_name.split())+"_", data, auth.user.id)
        db(db.userfiles.id == form.vars.id).update(time=time.time() + 60*2, owner=auth.user.id)
        redirect(URL('userAdd'))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form, data=data, station=station)
