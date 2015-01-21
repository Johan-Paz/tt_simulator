#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: japaz

import yaml
from os import path
import re
import numbers

class Environment(object):

	def __init__(self,envfile=None,environment=None,verbosity=False):
		# Reading configuration
		if not envfile:
			envfile = path.join(path.dirname(__file__),"..","conf","environment.yaml")
		with open(envfile) as config_file:
			config_content = config_file.read()
			self._config = yaml.load(config_content.replace('\t','   '))
			env_selected = None
			if not environment:
				env_selected = self.get('environment')
			elif environment in self._config:
				env_selected = environment

			if env_selected:
				if verbosity:
					print 'INFO: selected enviroment "%s"' % env_selected
				self._config = self._config[env_selected]
			elif 'default' in self._config:
				print 'WARNING: selected default environment!'
				self._config = self._config['default']

	def _find_in_map(self,cad,map):
		elements = cad.strip().split('.')
		for element in elements:
			if not element in map:
				return None
			map = map[element]

		return map


	def get(self,data):
		return self._find_in_map(data,self._config)

	def recall(self,cad):
		'''
		This function takes a string, look for:

		1. <#tokens#>: for substituting it for a value in world.c
		2. <#config.tokens#>: for substituting it for a value in world.config
		3. some texts declared to be substituted in Sketchs --> Substitutions

		'''
		tp = re.compile(r'<:([A-Za-z0-9.]*):>')

		possibles = tp.findall(cad)
		value = None
		for toChange in possibles:
			value = self.get(toChange)
			if value and (isinstance(value, numbers.Number)):
				value = str(value)

			if value and (isinstance(value,str) or isinstance(value,unicode)):
				cad = re.sub('<:' + toChange + ':>', value, cad)

		return cad

