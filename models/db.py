# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager
from gluon.tools import Recaptcha
from gluon.utils import web2py_uuid

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# auth.settings.captcha = Recaptcha(request, '6LcD0w4UAAAAALjOvI7bFgcbWOux6VipvnVAy3Hb', '6LcD0w4UAAAAACG4UdkBs-rq4Eg4srqTWGfl7_Rv')

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

if not auth.is_logged_in():
    if 'anon_user_uid' not in request.cookies:
        response.cookies['anon_user_uid'] = web2py_uuid()
        response.cookies['anon_user_uid']['path'] = '/'
        response.cookies['anon_user_uid']['expires'] = 7 * 24 * 3600
# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------

db._common_fields.append(auth.signature)

db.define_table('url', Field('long_url', 'text', requires=IS_URL()),
                Field('short_code', 'string', label="Short URL"),
                Field('created_by_anon', 'string'))


db.define_table('log_visit',
                Field('url', db.url),
                Field('referer_url', 'string', default='Other'),
                Field('browser', 'string', default='Other'),
                Field('platform', 'string', default='Other'),
                Field('processed', 'boolean', default=False))

db.define_table('referer_stats',
                Field('url', db.url),
                Field('stat_day', 'date'),
                Field('referer_url', 'string', default='Other'),
                Field('hit_count', 'double'))

db.define_table('browser_stats',
                Field('url', db.url),
                Field('stat_day', 'date'),
                Field('browser', 'string', default='Other'),
                Field('hit_count', 'double'))

db.define_table('platform_stats',
                Field('url', db.url),
                Field('stat_day', 'date'),
                Field('platform', 'string', default='Other'),
                Field('hit_count', 'double'))

db.url.short_code.readable = False
db.url.short_code.writable = False
db.url.created_by_anon.readable = False
db.url.created_by_anon.writable = False
db.url.long_url.widget = SQLFORM.widgets.string.widget
db.url.long_url.represent = lambda long_url, row: A(long_url, _href=long_url, _target="_blank")
db.url.created_on.represent = lambda created_on, row: created_on.strftime('%b %d, %Y') if created_on else ''
db.url.short_code.represent = lambda short_code, row: _create_short_url(short_code)

auth.enable_record_versioning(db)


def _create_short_url(short_code):
    """
    """
    if short_code:
        copy = DIV(SPAN(host() + short_code), BUTTON('copy', _type="button", _title="Copy to Clipboard", _class="btn btn-default btn-xs copy-button"))
        return copy


def host():
    """
    URL(host=True) is giving http://127.0.0.1:8000/url_grid.load.
    this function returns domain name
    """
    return '%s://%s/' % (request.env.get('wsgi_url_scheme',
                                         'http').lower(), request.env.http_host)