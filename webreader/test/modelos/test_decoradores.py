#!/usr/bin/env python

import unittest
from webreader.modelos.decoradores import TablaHtml
from webreader.modelos.decoradores import CampoTablaHtml


RUTA_XPATH = '/html/body'

@TablaHtml(ruta_xpath=RUTA_XPATH,fila_inicio=0,filas_sin_leer_al_final=0)
class ModeloDecoradoPrueba(object):
    
    @CampoTablaHtml(columna=4,ruta_adicional='/a/font')
    def propiedad1(self):
	pass

    @CampoTablaHtml(columna=3,ruta_adicional='/a/font')
    def propiedad2(self):
	pass


class CampoTablaHtmlTestCase(unittest.TestCase):
    """ Tests del decorador CampoTablaHtml. """
    

    def setUp(self):
        pass
	

    def test_atributos_correctos(self):
        """Comprueba que los atributos se pasan a los campos."""
        self.assertEqual(RUTA_XPATH,ModeloDecoradoPrueba.table_html_attr.ruta_xpath)
        
        
#Comprobar que solo se pasen atributos validos para cada decorador sino Excepc.

#Comprobar que las funciones decoradas sean propiedades y tengan setters
#Comprobar que TablaHtml decora una clase