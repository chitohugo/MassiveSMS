# -*- coding: utf-8 -*-
from gluon import current
import json
import serial
import pg
import time
import gammu
import sys
import types

class Enviar(object):	
	def __init__(self):
		self.db = current.db
		self.session = current.session
		self.request = current.request
		self.response = current.response
		self.cache = current.cache

	def guardarMensaje(self, post):
		type = isinstance(post['celulares[]'], types.StringType)
		if type == True:			
			post['destino'] = post['celulares[]']
			post['mensaje'] = post['mensaje']
			post['fk_municipio_id'] = post['mun']
			post['fk_cargo_id'] = post['carg']
			respuesta = self.db.estado_mensaje.validate_and_insert(
                    **self.db.estado_mensaje._filter_fields(post)).as_dict()		
			if len(respuesta['errors']) > 0:
				respuesta = dict(estatus=500, errors=respuesta['errors'], data={})
			else:
				respuesta = dict(estatus=200, errors={}, data=respuesta['id'])
			return respuesta
		else:
			for num in post['celulares[]']:			
				post['destino'] = num
				post['mensaje'] = post['mensaje']
				post['fk_municipio_id'] = post['mun']
				post['fk_cargo_id'] = post['carg']
				respuesta = self.db.estado_mensaje.validate_and_insert(
	                    **self.db.estado_mensaje._filter_fields(post)).as_dict()		
			if len(respuesta['errors']) > 0:
				respuesta = dict(estatus=500, errors=respuesta['errors'], data={})
			else:
				respuesta = dict(estatus=200, errors={}, data=respuesta['id'])
			return respuesta

	def listMenSalida(self):
		respuesta = self.db(self.db.estado_mensaje.estado == 1).select(self.db.estado_mensaje.estado).as_list()
		if len(respuesta) > 0:
			return len(respuesta)
		else:
			return len(respuesta)
		

	def enviarMensaje(self):
		while True:				
			try:
				sm = gammu.StateMachine()
				sm.ReadConfig()
				sm.Init()			
				respuesta = self.db(self.db.estado_mensaje.estado == 1).select(self.db.estado_mensaje.ALL).as_list()
				if len(respuesta) > 0:
					for data in respuesta:
						celular = data['destino']
						mensaje = data['mensaje']
						message = { 'Coding': 'Default_No_Compression','Text': mensaje,'Class': -1,'SMSC':{'Location': 1},'Number': celular,}				
						sm.SendSMS(message)
						actualizarEstadoMensaje = self.db(self.db.estado_mensaje.estado == 1).validate_and_update(estado = 0).as_dict()
						respuesta = dict(estatus=200, data="Mensajes enviado con exito...!")				
					return respuesta
				else:
					return "No hay mensaje para enviar"
			except gammu.ERR_GETTING_SMSC:
				return "NO SE HA ENCONTRADO NUMERO SMSC DEL MODEM O CELULAR."	
			except gammu.ERR_TIMEOUT:
				return "VERIFIQUE LA CONEXION DEL MODEM."
			except gammu.ERR_UNKNOWN:
				return "SIN SALDO SUFICIENTE PARA EL ENVIO DE MENSAJES...!"
			except gammu.ERR_DEVICENOTEXIST:
				return "NO HAY DISPOSITIVO CONECTADO."
			except gammu.ERR_DEVICEOPENERROR:
				return "ERROR ABRIENDO DISPOSITIVO. DESCONOCIDO, OCUPADO O SIN PERMISOS."
			except gammu.ERR_DEVICEWRITEERROR:
				return "ERROR ESCRIBIENDO EN EL DISPOSITIVO."
		
