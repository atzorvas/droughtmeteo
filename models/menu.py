response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description

response.menu = [
    (T('Home'), URL('default', 'index') == URL(), URL('default', 'index'), []),

    (T('Drought Indices Chart'), URL('stations', 'charts') == URL(), URL('stations', 'charts'), []),
    (T('SPI Calculator'), URL('stations', 'userAdd') == URL(), URL('stations', 'userAdd'), []),
    (T('About Drought'), URL('default', 'about') == URL(), URL('default', 'about'), []),
    (T('Contact Us'), URL('default', 'contact') == URL(), URL('default', 'contact'), []),
    (T('Further Development'), URL('default', 'further') == URL(), URL('default', 'further'), []),
]

if auth.has_membership(role = 'admin'):
    response.menu.insert(1, (T('Admin Panel'), URL('admin', 'panel') == URL(), URL('admin', 'panel'),
                             [
                              (T('Add Station'), URL('stations', 'add') == URL(), URL('stations', 'add')),
                              (T('View Station DataSets'), URL('stations', 'show') == URL(), URL('stations', 'show')),
                              (T('Edit Station'), URL('stations', 'edit') == URL(), URL('stations', 'edit')),
                              (False, False, LABEL('-- Admin Actions --')),
                              (False, False, A('Update Stations', _class="admin-menu", _href="#", _onclick="ajax('"+URL('admin', 'updateStations')+"',[''],':eval');jQuery('.flash').html('Please Wait...').slideDown();")),
                              (False, False, A('Update Charts', _class="admin-menu", _href="#", _onclick="ajax('"+URL('admin', 'updateCharts')+"',[''],':eval');jQuery('.flash').html('Please Wait...').slideDown();")),
                              (False, False, A('Update Estimation/Map', _class="admin-menu", _href="#", _onclick="ajax('"+URL('admin', 'updateMap2')+"', ['header'],':eval');jQuery('.flash').html('Please Wait...').slideDown().delay(2000).slideUp();")),
                              (T('Manage Accounts'), URL('admin', 'list_users') == URL(), URL('admin', 'list_users')),
                             ]
    ))
