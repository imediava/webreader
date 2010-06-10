
import unittest
from test import test_support
from webreader.extraccion.acceso import AccesoHTTP


class ConexionPOSTTestCase(unittest.TestCase):

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
	self.datosUsuario = {}
	self.datosUsuario['usuario'] = 'imediava'
        self.datosUsuario['clave'] = 'quetepet'
        self.datosUsuario['control'] = '1'
	self.url_conexion_buena = 'http://supermanager.acb.com/index.php'
	self.access = AccesoHTTP()
	

    def test_autentif_con_cookies(self):
        # Comprueba que se puede autentificar con un POST y con cookies.
	self.access.iniciarConexion(self.url_conexion_buena,self.datosUsuario)
	resp = self.access.obtenerRespuesta('http://supermanager.acb.com/' \
					    'vermercado.php?id_pos=1')
	self.assertEqual(200, resp.getcode())
	
    
    
if __name__ == '__main__':
    unittest.main()


	
	

