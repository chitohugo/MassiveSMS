# -*- coding: utf-8 -*-
import json
from Enviar import Enviar
enviar = Enviar()

@auth.requires_login()
def guardarMensaje():
	if request.ajax:
		response.view = "generic.json"		
		respuesta = enviar.guardarMensaje(request.post_vars)		
		respuesta = json.dumps(respuesta)		
		return respuesta		
	else:
		return dict()
@auth.requires_login()
def enviarMensaje():
	if request.ajax:
		response.view = "generic.json"
		respuesta = enviar.enviarMensaje()		
		respuesta = json.dumps(respuesta)		
		return respuesta		
	else:
		return dict()

