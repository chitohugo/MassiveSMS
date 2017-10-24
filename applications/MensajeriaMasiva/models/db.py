#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import gmtime, strftime
from gluon.custom_import import track_changes 
track_changes(True)
from gluon import current
from pydal import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')  


if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

from gluon.contrib.appconfig import AppConfig
myconf = AppConfig(reload=True)


uri = "postgres://chito:yndrid@localhost/massivesms"
current.db = DAL(uri,pool_size=1, check_reserved=['all'], lazy_tables=False, migrate=False)

current.db.define_table('municipio',                              
                Field('descripcion', type='string', length=20, required=True, notnull=True,
                    requires=[IS_NOT_EMPTY(error_message=('Este campo no puede ser vacio'))]),                                                                       
                )
current.db.define_table('cargo',                
                Field('descripcion', type='string', length=20, required=True, notnull=True,
                    requires=[IS_NOT_EMPTY(error_message=('Este campo no puede ser vacio'))]),                                                   
                )
current.db.define_table('mun_cargo',
                    Field('fk_municipio', 'reference municipio'),
                    Field('fk_cargo', 'reference cargo'),
                    primarykey=['fk_municipio','fk_cargo'],
                )
current.db.define_table('contacto',
                Field('numero', type='string', length=11, required=True, notnull=True,unique=True,
                    requires=[IS_NOT_EMPTY(error_message=('Este campo no puede ser vacio'))]),
                Field('fk_municipio_id', 'reference municipio',required=True),
                Field('fk_cargo_id', 'reference cargo',required=True),               
                )
current.db.define_table('estado_mensaje',
                Field('estado', length=1, required=True, notnull=True,default=1),
                Field('estado_envio',length=1,required=True, notnull=True,default=1),
                Field('fk_municipio_id', 'reference municipio',required=True),
                Field('fk_cargo_id', 'reference cargo',required=True),
                Field('destino',length=11,required=True, notnull=True),
                Field('mensaje',length=160,required=True, notnull=True),
                )


# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []

response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''



from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(current.db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=True, signature=False)

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
