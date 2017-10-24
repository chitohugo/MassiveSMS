# -*- coding: utf-8 -*-
from gluon import current
import json


class Numeros(object):	
	def __init__(self):
		self.db = current.db
		self.session = current.session
		self.request = current.request
		self.response = current.response
		self.cache = current.cache

	def buscarNumeros(self,idmun,idcarg):
		respuesta = self.db((self.db.contacto.fk_municipio_id == idmun) & 
							(self.db.contacto.fk_cargo_id == idcarg)).select(self.db.contacto.numero).as_list()
		return respuesta

		