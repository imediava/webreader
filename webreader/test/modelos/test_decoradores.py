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
COLUMNA3 = 5
RUTA_ADICIONAL = '/a/font'
LAMBDA_DOBLE = lambda x: 2*x
DECIMAL_PRUEBA = True

@TablaHtml(ruta_xpath=RUTA_XPATH,fila_inicio=FILA_INI,filas_sin_leer_al_final=FILA_FIN)
class ModeloDecoradoPrueba(object):
    """ Inner class for testing purposes."""
    
    @CampoTablaHtml(columna=COLUMNA1,ruta_adicional=RUTA_ADICIONAL)
    def field1(self):
        pass
    
    @CampoTablaHtml(columna=COLUMNA2,ruta_adicional=RUTA_ADICIONAL)
    def field2(self):
        pass

    @CampoTablaHtml(columna=COLUMNA3,tratar_valor=LAMBDA_DOBLE)
    def field3(self):
        pass
    
    @CampoTablaHtml(columna=COLUMNA3,decimal=DECIMAL_PRUEBA)
    def field4(self):
        pass
    
    
class TablaHtmlTestCase(unittest.TestCase):
    """ Decorators tests.
    
    Test for decorators TablaHtml y CampoTablaHtml.
    
    """
    
    def setUp(self):
        self.table = ModeloDecoradoPrueba.table_html_attr
        self.column1 = self.table.get_column('field1')
        self.column2 = self.table.get_column('field2')
	self.column3 = self.table.get_column('field3')
	self.column4 = self.table.get_column('field4')
    

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
        
        #Comprobar asignacion atributo tratar_valor
        self.assertEqual(LAMBDA_DOBLE, self.column3.tratar_valor)
        
        #Comprobar asignacion atributo decimal
        self.assertEqual(DECIMAL_PRUEBA, self.column4.decimal)
        
        #Comprobar atributos por defecto
        self.assertEqual(False,self.column1.decimal)
        self.assertEqual('',self.column3.ruta_adicional)
        
        

# Comprobar que no haya dos campos anotados y que tienen el mismo nombre
# Ej: @Campo...field1 y @Campo....field1 porque entonces se queda con los
# parametros de configuracion del segundo