
import unittest
from test import test_support
from webreader.extraccion.acceso import AccesoHTTPSupermanager
from webreader.extraccion.acceso import HTTP_CODE_OK
from webreader.extraccion.acceso import HTTP_CODE_ACCEPTED
from webreader.extraccion.acceso import CAMPO_AUTENTIF_USUARIO
from webreader.extraccion.acceso import CAMPO_AUTENTIF_CLAVE 
from webreader.extraccion.acceso import CAMPO_AUTENTIF_CONTROL
from webreader.extraccion.acceso import ErrorAutentificacionSupermanager
from webreader.extraccion.acceso import ErrorCamposAutentificacionSupermanager


class AccesoHTTPSupermanagerTestCase(unittest.TestCase):
    

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
	
    def test_fallo_autentif(self):
        # Comprueba que salta excepcion si la autentificacion no es correcta
	self.datosUsuario[CAMPO_AUTENTIF_CLAVE] = self.claveIncorrecta
	self.assertRaises(ErrorAutentificacionSupermanager,
			  self.access.iniciarConexion,
			  self.url_conexion_buena , self.datosUsuario)
	
    def test_fallo_autentif_campos_incorrectos(self):
        # Comprueba que salta excepcion si los campos de autentificacion pasados
	# no son correctos
	self.datosUsuario['campofalso'] = 'valorfalso'
	self.assertRaises(ErrorCamposAutentificacionSupermanager,
			  self.access.iniciarConexion,
			  self.url_conexion_buena , self.datosUsuario)
	
	
    def test_acceso_pagina_sin_conexion(self):
	# Comprueba que puede acceder a una URL sin necesidad de iniciar conex.
	resp = self.access.obtenerRespuesta(self.url_conexion_buena)
	self.assertEqual(HTTP_CODE_OK, resp.getcode())
	
    def test_acceso_obtener_fichero_pagina(self):
	# Comprueba que el texto de obtenerRespuesta() es igual a lo que
	# devuelve obtenerFicheroPagina()
	self.assertEqual(self.access.obtenerRespuesta(self.url_conexion_buena)
			 .read() ,
			 self.access
			 .obtenerFicheroPagina(self.url_conexion_buena))
        
if __name__ == '__main__':
    unittest.main()


	
	

