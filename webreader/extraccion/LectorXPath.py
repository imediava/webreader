#!/usr/bin/python
# -*- coding: latin-1 -*-
from BeautifulSoup import BeautifulSoup



ETIQUETAS_NO_RECONOCIDAS = ['tbody','thead']

ELEMENTO_CON_INDICE = r'^(?P<palabra>[\w]+)\[(?P<numero>[\d]+)\]$'
ELEMENTO_SIMPLE = r'^(?P<palabra>[\w]+)$'
ATRIBUTO_SIN_VALOR = r'^@(?P<atributo>[\w]+)$'


class LectorWebsXPath:
	""" Lector de elementos de paginas web reconocidos por su ruta xpath.
	
	Realiza traducciones de XPath a BeautifulSoup que es el lector con el
	que obtiene los elementos."""

	def __init__(self,cadenahtml):
		self.lectorBS = BeautifulSoup(cadenahtml)

	def obtener_todos(self,xpath,elem):
		""" Obtiene todos las tags del tipo elem justo debajo de xpath."""
		return eval('self.lectorBS%s.findAll(\'%s\')' % (toBeautifulSoup(xpath),elem))


	def obtener_elemento(self,xpath):
		#import logging
		#logging.info('self.lectorBS' + toBeautifulSoup(xpath))
		return eval('self.lectorBS' + toBeautifulSoup(xpath))

	def obtener_valor(self,xpath):
		"""Obtiene el valor del elemento no el elemento en si."""
		res_xpath_eval = self.obtener_elemento(xpath)
		if isinstance(res_xpath_eval,unicode):
			return unicode(res_xpath_eval)
		elif len(res_xpath_eval.contents) > 0:
			return unicode(res_xpath_eval.contents[0])
		else:
			return unicode(res_xpath_eval.string)



class LectorTablasHtmlXPath(LectorWebsXPath):

	def obtener_valor_celda(self,xpathtabla,fila,columna,decimal=False,ruta_adicional=''):
		valor = self.obtener_valor(self.obtener_xpath_celda(xpathtabla,fila,columna) + ruta_adicional)	
		if decimal:
			return tofloat(valor)
		return valor

	def obtener_xpath_celda(self,xpathtabla,fila,columna):
		return "%s/tr[%s]/td[%s]" % (xpathtabla,fila,columna)	 

import locale
#Asigna como local el es_UTF8
#locale.setlocale(locale.LC_ALL,'es_UTF8')
def tofloat(cadena):
	return float(cadena.replace(',','.'))
	#return str(locale.atof(cadena))

def toBeautifulSoup(xpath):
	"""Traduce una expresion xpath a su forma de acceso con BeautifulSoup.
	La expresión debe ser simple y contener solo elementos anidados (con  \\) y
	atributos (con @).
	
	Ej de expresion xpath aceptada: /html/body/a/@href """
	import re
	expresionBS = ''
	for paso in xpath.split('/')[1:]:
	  if re.match(ELEMENTO_SIMPLE,paso):
	      match = re.match(ELEMENTO_SIMPLE,paso)
	      if not match.group('palabra') in ETIQUETAS_NO_RECONOCIDAS:
		expresionBS += '.' + match.group('palabra')

	  elif (re.match(ELEMENTO_CON_INDICE,paso)):
	      match = re.match(ELEMENTO_CON_INDICE,paso)
	      if not match.group('palabra') in ETIQUETAS_NO_RECONOCIDAS:
              	expresionBS += '(\'' + match.group('palabra') + '\',recursive=False)[' + \
				str(int(match.group('numero')) -1) + ']'

	  elif (re.match(ATRIBUTO_SIN_VALOR,paso)):
	      match = re.match(ATRIBUTO_SIN_VALOR,paso)
	      expresionBS += '[\'' + match.group('atributo') + '\']'
	
	return expresionBS

#XPath: /html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[3]/td/a
#Traducido a BeautifulSoup = soup.html.body('table',recursive=False)[1].tr('td',recursive=False)[2].table('tr',recursive=False)[2]('td',recursive=False)[0].a.string

#1. Para x[n] en XPath en BS -> ('x',recursive=False)[n-1]
#2. tbody BS no lo toma asi que no ponerlos, saltar a su hijo por ejemplo XPath table.tbody.tr en BS -> table.tr

if __name__ == '__main__':
	xpathExp = '/html/body/table[2]/tr/td[3]/table/tr[3]/td[2]'
	print toBeautifulSoup(xpathExp)
