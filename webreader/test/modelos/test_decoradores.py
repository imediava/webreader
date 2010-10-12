#!/usr/bin/env python

import unittest

from webreader.modelos.decoradores import TablaHtml
from webreader.modelos.decoradores import CampoTablaHtml

# Table values
RUTA_XPATH = '/html/body'
FILA_INI=3
FILA_FIN=4

# Columns values
COLUMNA1 = 4
COLUMNA2 = 3
RUTA_ADICIONAL = '/a/font'

@TablaHtml(ruta_xpath=RUTA_XPATH,fila_inicio=FILA_INI,filas_sin_leer_al_final=FILA_FIN)
class ModeloDecoradoPrueba(object):
    """ Inner class for testing purposes."""
    
    @CampoTablaHtml(columna=COLUMNA1,ruta_adicional=RUTA_ADICIONAL)
    def field1(self):
        pass
    
    @CampoTablaHtml(columna=COLUMNA2,ruta_adicional=RUTA_ADICIONAL)
    def field2(self):
        pass

class CampoTablaHtmlTestCase(unittest.TestCase):
    """ Tests del decorador CampoTablaHtml. """
    
    def setUp(self):
        self.table = ModeloDecoradoPrueba.table_html_attr
        self.column1 = self.table.get_column('field1')
        self.column2 = self.table.get_column('field2')
	
    

    def test_atributos_correctos_tabla(self):
        """Checks the correct assignment of Table attributes."""
        self.assertEqual(RUTA_XPATH,self.table.ruta_xpath)
        self.assertEqual(FILA_INI,self.table.fila_inicio)
        self.assertEqual(FILA_FIN,self.table.filas_sin_leer_al_final)
        
        
    def test_atributos_correctos_campos(self):
        """Checks the correct assignment of Column attributes."""
        #Comprobar asignaciones del atributo columna
        self.assertEqual(COLUMNA1,self.column1.columna)
        self.assertEqual(COLUMNA2,self.column2.columna)
        
        #Comprobar asignaciones del atributo ruta_adicional
        self.assertEqual(RUTA_ADICIONAL,self.column1.ruta_adicional)
        self.assertEqual(RUTA_ADICIONAL,self.column2.ruta_adicional)
        
#Comprobar que solo se pasen atributos validos para cada decorador sino Excepc.

#Comprobar que TablaHtml decora una clase