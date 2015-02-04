# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=20)#,check_reserved=['postgres', 'mssql'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login

db.define_table('stations',
                Field('name', 'string'),
                Field('city', 'string'),
                Field('state', 'string'),
                Field('emy_file', 'upload'),
                Field('noa_url', 'string'),
                Field('lat', 'string'),
                Field('long', 'string'),
                Field('elev', 'string'),
                Field('data_from', 'string'),
                Field('data_to', 'string'),
                Field('data_list', 'list:string'),
                Field('temp_data_list', 'list:string'),
                format='%(name)s')

db.stations.name.requires = [IS_LENGTH(maxsize=30, minsize=3, error_message='must be from 5 to 30 chars'), IS_NOT_IN_DB(db, 'stations.name')]
db.stations.city.requires = IS_NOT_EMPTY()
db.stations.noa_url.requires = IS_NOT_IN_DB(db, 'stations.noa_url')
db.stations.lat.requires = IS_NOT_EMPTY()
db.stations.long.requires = IS_NOT_EMPTY()

db.define_table('noadata',
                Field('station_id', db.stations),
                Field('year', 'integer'),
                Field('jan', 'double'),
                Field('feb', 'double'),
                Field('mar', 'double'),
                Field('apr', 'double'),
                Field('may', 'double'),
                Field('jun', 'double'),
                Field('jul', 'double'),
                Field('aug', 'double'),
                Field('sep', 'double'),
                Field('oct', 'double'),
                Field('nov', 'double'),
                Field('dec', 'double'),
                )

db.define_table('alldata',
                Field('station_id', db.stations),
                Field('year', 'integer'),
                Field('jan', 'double'),
                Field('feb', 'double'),
                Field('mar', 'double'),
                Field('apr', 'double'),
                Field('may', 'double'),
                Field('jun', 'double'),
                Field('jul', 'double'),
                Field('aug', 'double'),
                Field('sep', 'double'),
                Field('oct', 'double'),
                Field('nov', 'double'),
                Field('dec', 'double'),
                primarykey=['station_id', 'year'])

db.define_table('emydata',
                Field('station_id', db.stations),
                Field('year', 'integer'),
                Field('jan', 'double'),
                Field('feb', 'double'),
                Field('mar', 'double'),
                Field('apr', 'double'),
                Field('may', 'double'),
                Field('jun', 'double'),
                Field('jul', 'double'),
                Field('aug', 'double'),
                Field('sep', 'double'),
                Field('oct', 'double'),
                Field('nov', 'double'),
                Field('dec', 'double'),
                primarykey=['station_id', 'year'])

db.noadata.station_id.requires =  db.emydata.station_id.requires =  db.alldata.station_id.requires = IS_IN_DB(db, db.stations.id, '%(name)s')


db.define_table('temp_noadata',
                Field('station_id', db.stations),
                Field('year', 'integer'),
                Field('jan', 'double'),
                Field('feb', 'double'),
                Field('mar', 'double'),
                Field('apr', 'double'),
                Field('may', 'double'),
                Field('jun', 'double'),
                Field('jul', 'double'),
                Field('aug', 'double'),
                Field('sep', 'double'),
                Field('oct', 'double'),
                Field('nov', 'double'),
                Field('dec', 'double'),
                )

db.define_table('temp_alldata',
                Field('station_id', db.stations),
                Field('year', 'integer'),
                Field('jan', 'double'),
                Field('feb', 'double'),
                Field('mar', 'double'),
                Field('apr', 'double'),
                Field('may', 'double'),
                Field('jun', 'double'),
                Field('jul', 'double'),
                Field('aug', 'double'),
                Field('sep', 'double'),
                Field('oct', 'double'),
                Field('nov', 'double'),
                Field('dec', 'double'),
                primarykey=['station_id', 'year'])

db.define_table('temp_emydata',
                Field('station_id', db.stations),
                Field('year', 'integer'),
                Field('jan', 'double'),
                Field('feb', 'double'),
                Field('mar', 'double'),
                Field('apr', 'double'),
                Field('may', 'double'),
                Field('jun', 'double'),
                Field('jul', 'double'),
                Field('aug', 'double'),
                Field('sep', 'double'),
                Field('oct', 'double'),
                Field('nov', 'double'),
                Field('dec', 'double'),
                primarykey=['station_id', 'year'])
db.temp_noadata.station_id.requires = db.temp_emydata.station_id.requires = db.temp_alldata.station_id.requires = \
    IS_IN_DB(db, db.stations.id, '%(name)s')


db.define_table('current',
                Field('station_id', db.stations),
                Field('value', 'string'),
                Field('spivalue'))
db.current.station_id.requires = IS_IN_DB(db, db.stations.id, '%(name)s')


db.define_table('userfiles',
                Field('station_name', 'string'),
                Field('userfile', 'upload'),
                Field('time'),
                Field('owner'))
db.userfiles.userfile.requires = db.userfiles.station_name.requires = IS_NOT_EMPTY()
db.userfiles.time.readable = db.userfiles.time.writable = False
db.userfiles.owner.readable = db.userfiles.owner.writable = False

from gluon.custom_import import track_changes
track_changes(True)
