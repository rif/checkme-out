# -*- coding: utf-8 -*-

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
response.optimize_css = 'concat,minify,inline'
response.optimize_js = 'concat,minify,inline'

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
from datetime import date
auth = Auth(db)
auth.settings.extra_fields['auth_user']= [
    Field('country'),
    Field('location'),
    Field('birth_date', 'date', default=date(1978,7,10)),
    Field('sex', requires=IS_IN_SET((T('Male'), T('Female')))),
]

crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail=auth.settings.mailer
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
use_janrain(auth,filename='private/janrain.key')


Photos = db.define_table('photo',
                         Field('title'),
                         Field('user', 'reference auth_user',
                               readable=False, writable=False,
                               default=auth.user_id),
                         Field('photo', 'upload'),
                         format='%(title)s'
)

Contests = db.define_table('contest',
                           Field('name'),
                           Field('country'),
                           Field('location'),
                           Field('gender',
                                 requires=IS_IN_SET((T('Male'), T('Female')))),
                           Field('min_age', 'integer'),
                           Field('max_age', 'integer'),
                           Field('admission_deadline', 'datetime'),
                           Field('voting_deadline', 'datetime'),
                           format='%(name)s'
)

Votes = db.define_table('vote',
                        Field('picture', 'reference picture',
                              required=True, notnull=True),
                        Field('contest', 'reference contest',
                              requires=IS_EMPTY_OR(IS_IN_DB(db,db.contest.id))),
                        Field('score', 'double',
                              requires=IS_DECIMAL_IN_RANGE(0, 10, dot=".")),
)


## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

a0, a1 = request.args(0), request.args(1)
