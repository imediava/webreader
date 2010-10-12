#!/usr/bin/python
# -*- coding: latin-1 -*-
from BeautifulSoup import BeautifulSoup
from collections import MutableMapping



ETIQUETAS_NO_RECONOCIDAS = ['tbody','thead']

ELEMENTO_CON_INDICE = r'^(?P<palabra>[\w]+)\[(?P<numero>[\d]+)\]$'
ELEMENTO_SIMPLE = r'^(?P<palabra>[\w]+)$'
ATRIBUTO_SIN_VALOR = r'^@(?P<atributo>[\w]+)$'


class LectorWebsXPath(object):
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
	
	def __init__(self,tabla_Html,cadenahtml):
		super(LectorTablasHtmlXPath,self).__init__(cadenahtml)
		self.tabla_Html = tabla_Html
	
	def obtener_tabla(self):
		""" Devuelve una tabla con el contenido de la tabla html."""
		# Crear tabla y rellenarla con contenido
		tabla = Tabla(self.tabla_Html.obtener_nombres_columnas())
		fila_fin = len(self.obtener_todos(self.tabla_Html.ruta_xpath,'tr'))
		ultima_fila_a_leer = fila_fin - self.tabla_Html.filas_sin_leer_al_final
		# Ahora se recorre las filas desde la inicial a la final ambas incluidas
		for num_fila in range(self.tabla_Html.fila_inicio,ultima_fila_a_leer + 1):
		    fila = Fila(self.tabla_Html.obtener_nombres_columnas())
		    for campo in self.tabla_Html.campos:
			valor_original = self._leer_campo(num_fila,campo)
			fila.set_cell(campo.nombre,campo.tratar_valor(valor_original))
		    tabla.add_row(fila)
		return tabla
		        
		
	def _leer_campo(self,fila,campo):
		return self._obtener_valor_celda(fila,campo.columna,campo.decimal,campo.ruta_adicional)

	def _obtener_valor_celda(self,fila,columna,decimal=False,ruta_adicional=''):
		valor = self.obtener_valor(self._obtener_xpath_celda(self.tabla_Html.ruta_xpath,fila,columna) + ruta_adicional)	
		if decimal:
			return tofloat(valor)
		return valor

	def _obtener_xpath_celda(self,xpathtabla,fila,columna):
		return "%s/tr[%s]/td[%s]" % (xpathtabla,fila,columna)
		

class ModeloTablaHTML(object):
	""" Esqueleto con los datos necesarios para leer una tabla HTML."""
	
	def __init__(self,campos,ruta_xpath,fila_inicio,filas_sin_leer_al_final):
		self.ruta_xpath = ruta_xpath
		self.fila_inicio = fila_inicio
		self.filas_sin_leer_al_final = filas_sin_leer_al_final
		self._campos = campos
	
	@property
	def campos(self):
		return self._campos
	
	def get_column(self,name):
		""" Gets the column by the name if it exists otherwise None."""
		campos = [ column for column
			in self.campos
			if column.nombre == name]
		if len(campos) == 1:
			return campos[0]
		else:
			return None
	
	def obtener_nombres_columnas(self):
		""" Gets the columns' names."""
		return [campo.nombre for campo in self.campos]
		
		
class ModeloColumnaTablaHTML(object):
	""" Datos para leer una columna de una tabla HTML."""
	
	def __init__(self,nombre,columna,tratar_valor=lambda x: x,decimal=False,ruta_adicional=''):
		"""
		
		"""
		self.nombre = nombre
		self.columna = columna
		self.decimal = decimal
		self.ruta_adicional = ruta_adicional
		self.tratar_valor = tratar_valor


class Tabla(object):
	""" Table object. """
	
	def __init__(self,column_names):
		""" Create the table.
		
		Keyword parameters:
		
		column_names -- List of names of the columns.
		
		"""
		self.row_count = 0
		self.dict = {}
		for col_name in column_names:
			self.dict[col_name] = []
	
	def add_row(self,row):
		""" Adds a row to the table. 		"""
		self.row_count += 1
		for col_name,value in self.dict.items():
			value.append(row[col_name])
	
	def get_row(self, row_index):
		""" Returns the row marked by row_index.
		
		Keyword parameters:
		
		row_index -- Index of the row to get
		
		"""
		row = {}
		for col_name,value in self.dict.items():
			row[col_name] = value[row_index]
		return row
	
	def get_all_rows(self):
		""" Devuelve un iterador sobre todas las filas de la tabla."""
		for row_index in range(0,self.row_count):
			yield self.get_row(row_index)
		
	
	def get_cell(self, column_name, row_index):
		""" Returns the cell marked by the column_name and the row_index.
		
		Keyword parameters:
		
		column_name -- Name of the cell's column
		row_index -- Index of the row
		
		"""
		return self.get_row(row_index)[column_name]
		

class Fila(MutableMapping):
	
	def __init__(self, column_names):
		""" Create the row.
		
		Keyword parameters:
		
		column_names -- List of names of the columns.
		
		"""
		self.dict = {}
		for col_name in column_names:
			self.dict[col_name] = []
	
	def set_cell(self, column_name, value):
		""" Set the value of a cell.
		
		Keyword parameters:
		
		column_name -- Name of the column
		value -- New value for the row
		
		"""
		self.dict[column_name] = value
		
	def get_cell(self,column_name):
		""" Returns the value of a cell."""
		return self.dict[column_name]
	
	def __setitem__(self,key,value):
		self.set_cell(key,value)
	
	def __getitem__(self,key):
		return self.get_cell(key)
		
	def __delitem__(self,key):
		del self.dict[key]
		
	def __iter__(self):
		self.dict.__iter__()
	
	def __len__(self):
		return self.dict.__len__()
		
		
		


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
