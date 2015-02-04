import datetime
import calendar
# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request, db)
def call(): return service()
### end requires


def index():
    session.forget(response)
    currentValues = db(db.current).select()
    stations = db(db.stations).select()
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    return dict(currentValues=currentValues, stations=stations, now=calendar.month_name[month], year=year)


def index2():
    session.forget(response)
    rows = db(db.current).select()
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    return dict(rows = rows)


def error():
    session.forget(response)
    return dict()


def about():
    session.forget(response)
    return dict()


def further():
    session.forget(response)
    return dict()


def contact():
    form = SQLFORM.factory(
        Field('your_email', requires=IS_EMAIL()),
        Field('subject', requires=IS_NOT_EMPTY()),
        Field('body', 'text', requires=IS_NOT_EMPTY()))
    form.element('#no_table_body')['_style'] = 'width:700px'
    if form.process().accepted:
        if mail.send(to=settings.email_sender,
                     reply_to='{}'.format(form.vars.your_email),
                     cc=form.vars.your_email,
                     bcc=['antonis@tzorvas.com', 'stavrosana@aegean.gr'],
                     subject='[GDM-Contact] {}'.format(form.vars.subject),
                     message='mail from: {}\n\n{}'.format(form.vars.your_email, form.vars.body)):
            response.flash = 'Thank you'
        else:
            form.errors.your_email = "Unable to send the email"
    return dict(form=form)