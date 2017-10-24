# -*- coding: utf-8 -*-
import json
from Cargos import Cargos
from Municipios import Municipios
from Numeros import Numeros
from Enviar import Enviar
from Usuarios import Usuarios
cargo = Cargos()
municipio = Municipios()    
numero = Numeros()
enviar = Enviar()
usuarios = Usuarios()

"""@auth.requires_login()
def index():
    return dict()"""



@auth.requires_login()
def index():
        
    if request.ajax:
        if request.get_vars['carg']>0:
            response.view = "generic.json"                  
            numeros = numero.buscarNumeros(request.get_vars['mun'],request.get_vars['carg'])
            numeros = json.dumps(numeros)
            return numeros  
        else:
            response.view = "generic.json"              
            cargos = cargo.buscarCargos(request.get_vars['mun'])
            cargos = json.dumps(cargos)         
            return cargos
    elif request:
        municipios = municipio.listarMunicipios()
        mensalida = enviar.listMenSalida()
        return dict(municipios=municipios,mensalida=mensalida)
    
    else:
        return dict()



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


