import urllib, urllib2
import csv
import cookielib
from webreader.utiles.enums import Enum

#TODO: Permitir al usuario introducir su nombre de usuario y clave
FICHERO_DATOS_USUARIO = 'WebContent/datosUsuarioSM.txt'
enumPosiciones = Enum("base","alero","pivot")

# Acceso General
HTTP_CODE_OK = 200
HTTP_CODE_ACCEPTED = 202
HTTP_CODE_FOUND = 302

#Supermanager

#Campos de autentificacion en el supermanager
CAMPO_AUTENTIF_USUARIO = 'usuario'
CAMPO_AUTENTIF_CLAVE = 'clave'
CAMPO_AUTENTIF_CONTROL = 'control'
		
# Acceso General
class AccesoHTTP(object):	

	def iniciarConexion(self,url,datos):
		# Procesador de cookies necesario para mantener la sesion
		# una vez autenticados con usuario y clave
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(opener)
		#Se codifican los datos para mandarlos en el POST
		authreq_data = urllib.urlencode(datos)
		return urllib2.urlopen(url,authreq_data)

	def obtenerFicheroPagina(self,url):
		return self.obtenerRespuesta(url).read()
		
		
	
	def obtenerRespuesta(self,url):
		auth_req = urllib2.Request(url)
		auth_resp = urllib2.urlopen(auth_req)
		return auth_resp



class AccesoHTTPSupermanager(AccesoHTTP):
	
	def __init__(self, datos={}, url_conex=""):
		if datos == {}:
			self.datosUsuario = {}
			self.datosUsuario[CAMPO_AUTENTIF_USUARIO] = 'imediava'
			self.datosUsuario[CAMPO_AUTENTIF_CLAVE] = 'quetepet'
			self.datosUsuario[CAMPO_AUTENTIF_CONTROL] = '1'
			
		if url_conex == "":
			self.url_conexion = 'http://supermanager.acb.com/index.php'
		
		self.iniciarConexion(self.url_conexion,self.datosUsuario)
			
	
	# Pagina a la que supermanager.acb.com redirecciona cuando la
	# autenticacion en index.php es correcta
	PAGINA_REDIRECCION = 'http://supermanager.acb.com/principal.php'

	def iniciarConexion(self,url,datos):
		campos_necesarios = [CAMPO_AUTENTIF_USUARIO, CAMPO_AUTENTIF_CLAVE,
				     CAMPO_AUTENTIF_CONTROL]
		#Comprueba que los campos a pasar para la autentif son correctos
		#print campos_necesarios
		lista_pasada = datos.keys()[:]
		campos_necesarios.sort()
		lista_pasada.sort()
		if campos_necesarios != lista_pasada:
			raise ErrorCamposAutentificacionSupermanager \
				(campos_necesarios, datos.keys)
			
		resp = super(AccesoHTTPSupermanager,self) \
			.iniciarConexion(url,datos)
		if resp.geturl() != self.PAGINA_REDIRECCION:
			raise ErrorAutentificacionSupermanager(url,datos)
		
class ErrorAutentificacionSupermanager(Exception):
	def __init__(self, urlAcceso, datosAcceso):
		self.url = urlAcceso
		self.datosUsuario = datosAcceso
	
	def __str__(self):
		return "Fallo al intentar acceder a %s" \
			" con datos de POST %s." % (self.url,self.datosUsuario)

class ErrorCamposAutentificacionSupermanager(Exception):
	def __init__(self, camposNecesarios, camposPasados):
		self.camposNecesarios = camposNecesarios
		self.camposPasados = camposPasados
	
	def __str__(self):
		return "Fallo son necesarios los siguientes campos %s" \
			" y se han pasado %s para autentificar." \
				% (self.camposNecesarios,self.camposPasados)