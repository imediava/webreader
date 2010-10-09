#!/usr/bin/env python

#!/usr/bin/python

from webreader.extraccion.LectorXPath import ModeloColumnaTablaHTML
from webreader.extraccion.LectorXPath import ModeloTablaHTML
import inspect

COLUMN_ATTR_KEY = 'column_html_attr'

class TablaHtml(object):

    def __init__(self,ruta_xpath, fila_inicio, filas_sin_leer_al_final):
    	self.ruta_xpath = ruta_xpath
    	self.fila_inicio = fila_inicio
    	self.filas_sin_leer_al_final = filas_sin_leer_al_final

    def __call__(self,clase):
        print clase
        campos = self._getColumns(clase)
        modelo_tabla = ModeloTablaHTML(campos = campos, ruta_xpath = self.ruta_xpath, \
                                       fila_inicio = self.fila_inicio, \
                                       filas_sin_leer_al_final = self.filas_sin_leer_al_final)
        clase.table_html_attr = modelo_tabla
        return clase
    
    def _getColumns(self,clase):
        """ Return the properties who will be read from a html table."""
        metodos_clase = inspect.getmembers(clase,lambda x : inspect.ismethod(x))
        campos = [ tupla[1].func_dict[COLUMN_ATTR_KEY] for tupla in metodos_clase \
                        if tupla[1].func_dict.has_key(COLUMN_ATTR_KEY)]
        return campos


class CampoTablaHtml(object):

    def __init__(self,columna, ruta_adicional):
    	self.columna = columna
    	self.ruta_adicional = ruta_adicional

    def __call__(self,function):
	function.func_dict[COLUMN_ATTR_KEY] = \
                    ModeloColumnaTablaHTML(nombre=function.func_name, \
                                           columna=self.columna,\
                                           ruta_adicional=self.ruta_adicional)
        return function




    
    

if __name__ == '__main__':
    print ModeloDecoradoPrueba.__dict__
