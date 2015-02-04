# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
import actions, getNewData, os

@auth.requires_membership('admin')
def delCharts():
    if actions.delCharts(os,request.folder):
        return 'jQuery(".flash").html("Charts Folder is now Empty!")\
           .slideDown().delay(1000).slideUp();'

@auth.requires_membership('admin')
def updateCharts():
    print "Update Charts.."
    session.forget(response)
    scheduler.queue_task('updateCharts', task_name='new', timeout=300)
    #actions.updateGraphs(os,db,request.folder)
    return 'jQuery(".flash").html("Charts Update: job sent").slideDown().delay(2000).slideUp();'

@auth.requires_membership('admin')
def updateMap2():
    session.forget(response)
    scheduler.queue_task('updateMaps', task_name='new', timeout=300)

@auth.requires_membership('admin')
def updateStations():
    for station in db(db.stations).select():
        item = getNewData.station(station.noa_url,station.data_to)
        actions.updateRain(db, session, station.id, vars(item)['_data'])
        actions.updateTemp(db, session, station.id, vars(item)['_data'])
        db(db.stations.id == station.id).update(data_to=vars(item)['_info']['to'])
    actions.calc_data(db, session, redirect, URL, request)
    msg = "OK"
    return 'jQuery(".flash").html("Stations Update: ' + msg + '").slideDown().delay(2000).slideUp();'


@auth.requires_membership('admin')
def clearAll():
    try:
        db(db.stations).delete()
        db(db.emydata).delete()
        db(db.noadata).delete()
        db(db.alldata).delete()
        db(db.temp_noadata).delete()
        db(db.temp_emydata).delete()
        db(db.temp_alldata).delete()
        db(db.current).delete()
        actions.delCharts(os,request.folder)
        msg = "OK"
    except:
        msg = "FAIL"
    return 'jQuery(".flash").html("Clearing GDM: ' \
           + msg + '").slideDown().delay(2000).slideUp();'

@auth.requires_membership('admin')
def index():
    #redirect(URL('default', 'index'))
    allItems = []

    update_charts = BUTTON('update charts', _id='btn1', _onclick="ajax('"+URL('updateCharts')+"',['btn1'],':eval')")
    allItems.append(update_charts)

    clear_db = BUTTON('clear charts', _id="btn2", _onclick="ajax('"+URL('delCharts')+"',['btn2'],':eval')")
    allItems.append(clear_db)

    update_maps = BUTTON('update maps', _id="btn3", _onclick="ajax('"+URL('updateMap')+"',['btn3'],':eval')")
    allItems.append(update_maps)

    update_current = BUTTON('update current', _id="btn4", _onclick="ajax('"+URL('updateCurrent')+"',['btn4'],':eval')")
    allItems.append(update_current)

    return dict(allItems=allItems)

@auth.requires_membership('admin')
def panel():
    allItems = []
    update_stations = BUTTON('Update Stations', _id="btn4", _onclick="ajax('"+URL('admin', 'updateStations')+"',[''],':eval');jQuery('.flash').html('Please Wait...').slideDown();")
    allItems.append(update_stations)
    update_charts = BUTTON('Update Charts', _id='btn1', _onclick="ajax('"+URL('admin', 'updateCharts')+"',[''],':eval');jQuery('.flash').html('Please Wait...').slideDown();")
    allItems.append(update_charts)
    update_maps = BUTTON('Update Estimation/Map', _id="btn3", _onclick="ajax('"+URL('admin', 'updateMap2')+"', ['header'],':eval');jQuery('.flash').html('Please Wait...').slideDown().delay(2000).slideUp();;")
    allItems.append(update_maps)

    if auth.user.username == "atzorvas" or auth.user.username == "stavrosana":
        clear_app = BUTTON('Clear App', _id='btn1', _onclick="ajax('"+URL('admin', 'clearAll')+"',[''],':eval');jQuery('.flash').html('Please Wait...').slideDown();")
        allItems.append(clear_app)
    return dict(items=allItems)

@auth.requires_membership('admin')
def list_users():
    btn = lambda row: A("Edit", _href=URL('editUser', args=row.auth_user.id))
    db.auth_user.edit = Field.Virtual(btn)
    rows = db(db.auth_user).select()
    headers = ["ID", "Username", "Name", "Last Name", "Email", "Edit"]
    fields = ['id', "username", 'first_name', 'last_name', "email", "edit"]
    table = TABLE(THEAD(TR(*[B(header) for header in headers])),
                  TBODY(*[TR(*[TD(row[field]) for field in fields]) \
                        for row in rows]))
    table["_class"] = "table table-striped table-bordered table-condensed"
    return dict(usersTable=table)

@auth.requires_membership('admin')
def editUser():
    this_user = db.auth_user(db.auth_user.id==request.args(0))
    res = db.auth_membership(db.auth_membership.user_id==request.args(0))
    this_role = res.group_id
    form = SQLFORM.factory(Field('firstName', default=this_user.first_name, label="First Name"),
                            Field('lastName', default=this_user.last_name, label="Last Name"),
                            #Field('password', 'password', default=this_user.password, label="Password"),
                            Field('role', requires=IS_IN_DB(db(db.auth_group.description=="custom group"),
                                          db.auth_group, '%(role)s', orderby=db.auth_group.id),
                                          default=this_role, widget=SQLFORM.widgets.radio.widget))
    form.add_button('All Users', URL('admin', 'list_users'))
    form.add_button('Admin Panel', URL('admin', 'panel'))
    if form.process(formname='form_two').accepted:
        response.flash = 'user profile changed'
        db(db.auth_user.id == this_user.id).update(first_name=request.vars.firstName, last_name=request.vars.lastName)
        db.auth_membership.update_or_insert(db.auth_membership.user_id==this_user.id, user_id=this_user.id, group_id=request.vars.role)
        #print len(res)
        redirect(URL('editUser', args=this_user.id))
    return dict(form=form)
