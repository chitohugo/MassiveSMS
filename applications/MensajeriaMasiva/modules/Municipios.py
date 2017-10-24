# -*- coding: utf-8 -*-
from gluon import current
from gluon.custom_import import track_changes 
track_changes(True)
import json


class Municipios(object):	
	def __init__(self):
		self.db = current.db
		self.session = current.session
		self.request = current.request
		self.response = current.response
		self.cache = current.cache

	def listarMunicipios(self):
		respuesta = self.db().select(self.db.municipio.ALL, orderby=self.db.municipio.descripcion)
		return respuesta

		
		