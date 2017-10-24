# -*- coding: utf-8 -*-

from gluon import current
import json


class Cargos(object):

	def __init__(self):
		self.db = current.db
		self.session = current.session
		self.request = current.request
		self.response = current.response
		self.cache = current.cache

	def buscarCargos(self,idmun):
		respuesta = self.db((self.db.mun_cargo.fk_municipio == idmun) & 
							(self.db.mun_cargo.fk_cargo == self.db.cargo.id)).select(self.db.cargo.ALL, 
								orderby=self.db.cargo.descripcion).as_list()
		return respuesta



