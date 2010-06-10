import urllib, urllib2
import csv
import cookielib
from webreader.utiles.enums import Enum

#TODO: Permitir al usuario introducir su nombre de usuario y clave
FICHERO_DATOS_USUARIO = 'WebContent/datosUsuarioSM.txt'
enumPosiciones = Enum("base","alero","pivot")


class AccesoHTTP:	

	def iniciarConexion(self,url,datos):
		# Procesador de cookies necesario para mantener la sesion
		# una vez autenticados con usuario y clave
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(opener)
		#Se codifican los datos para mandarlos en el POST
		authreq_data = urllib.urlencode(datos)
		urllib2.urlopen(url,authreq_data)

	def obtenerFicheroPagina(self,url):
		return self.obtenerRespuesta(url).read()
		
		
	
	def obtenerRespuesta(self,url):
		auth_req = urllib2.Request(url)
		auth_resp = urllib2.urlopen(auth_req)
		return auth_resp

