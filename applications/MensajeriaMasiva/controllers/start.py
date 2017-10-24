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


"""def login():
	if request.ajax:
		respuesta = usuarios.validarInicioSesion(request.vars)
		respuesta = json.dumps(respuesta)
		return respuesta
	else:
		return dict()"""



#@auth.requires_login()
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

