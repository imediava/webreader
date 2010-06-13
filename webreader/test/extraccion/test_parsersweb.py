#!/usr/bin/env python
import unittest
from test import test_support

class ParserJugadoresTestCase(unittest.TestCase):
    

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
	self.claveIncorrecta = 'incorrecta'
	self.datosUsuario = {}
	self.datosUsuario[CAMPO_AUTENTIF_USUARIO] = 'imediava'
        self.datosUsuario[CAMPO_AUTENTIF_CLAVE] = 'quetepet'
        self.datosUsuario[CAMPO_AUTENTIF_CONTROL] = '1'
	self.url_conexion_buena = 'http://supermanager.acb.com/index.php'
	self.url_despues_conexion = 'http://supermanager.acb.com/' \
			     'vermercado.php?id_pos=1'
	self.access = AccesoHTTPSupermanager()
	

    def test_autentif_con_cookies(self):
        # Comprueba que se puede autentificar con un POST y con cookies.
	self.access.iniciarConexion(self.url_conexion_buena,self.datosUsuario)
	resp = self.access.obtenerRespuesta(self.url_despues_conexion)
	self.assertEqual(HTTP_CODE_OK, resp.getcode())
	self.assertEqual(self.url_despues_conexion,resp.geturl())

