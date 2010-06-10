from StringIO import StringIO
from webreader.modelos.jugador import Jugador
import acceso
from LectorXPath import LectorTablasHtmlXPath,LectorTablasHtmlXPath,toBeautifulSoup

class ParserHtml:
    """ Contiene metodos comunes para tratar el acceso a web """
    
    def __init__(self,cadenaHtml,filtroxpath):
        """
        Inicializa el parser 
        """
        self.cadenaHtml = cadenaHtml
        self.filtroxpath = filtroxpath
        
    #Obtiene una lista de los jugadores de una posicion
    def obtenerArbolFiltrado(self):
        tree = self.obtenerArbolXml(self.cadenaHtml)
        return self.filtrarArbol(tree)
    
    @staticmethod
    def obtenerArbolXml(cadenaHtml):
        """Parsear archivo html"""
        f = StringIO(cadenaHtml)
        parser = etree.HTMLParser()
        tree = etree.parse(f,parser)
        return tree 
        
    def filtrarArbol(self,tree):
        return tree.xpath(self.filtroxpath)
 

class ParserJugadores(ParserHtml):

    def __init__(self,posicion,cadena=None):
        """Si recibe el argumento cadena ignora la posicion.
        Sino busca la url de supermanager.acb.com donde esta la lista
        de jugadores para esa posicion"""
	datosUsuario = {}
	datosUsuario['usuario'] = 'imediava'
	datosUsuario['clave'] = 'quetepet'
	datosUsuario['control'] = '1'
	url_conexion = 'http://supermanager.acb.com/index.php'
        self.posicion = posicion
        if not cadena:
            url = self.getUrlPosicion(posicion)
	    import logging
	    logging.info(url)
	    acceso_conex = acceso.AccesoHTTP()
	    acceso_conex.iniciarConexion(url_conexion,datosUsuario)
            cadena = acceso_conex.obtenerFicheroPagina(url)
	
	self.lectorXPath = LectorTablasHtmlXPath(cadena)	
    
    
    def parsearlista(self):
	xpathtabla = '/html/body/table[2]/tbody/tr/td[3]/table[2]/tbody'
	fila_inicio = 3
	fila_fin = len(self.lectorXPath.obtener_todos(xpathtabla,'tr'))
        lista = []
	for i in range(fila_inicio,fila_fin):
		jugador = Jugador()
		jugador.nombre = self.lectorXPath.obtener_valor_celda(xpathtabla,i,4,ruta_adicional='/a/font')
		jugador.website = self.lectorXPath.obtener_valor_celda(xpathtabla,i,4,ruta_adicional='/a/@href')
		jugador.val_jornada = self.lectorXPath.obtener_valor_celda(xpathtabla,i,11,decimal=True)
		jugador.val_ultimas3 = self.lectorXPath.obtener_valor_celda(xpathtabla,i,12,decimal=True)
		jugador.subir15 = self.lectorXPath.obtener_valor_celda(xpathtabla,i,13,decimal=True)
		jugador.precio = int(self.lectorXPath.obtener_valor_celda(xpathtabla,i,9).replace(".",""))
		jugador.val_media = self.lectorXPath.obtener_valor_celda(xpathtabla,i,8,decimal=True)
		jugador.equipo = self.lectorXPath.obtener_valor_celda(xpathtabla,i,6)
		jugador.posicion = str(self.posicion)
		#import logging
		#logging.error('Jugador:' + str(jugador))
                lista.append(jugador)
                
        return lista

      
    
    def getUrlPosicion(self,posicion):
        """Devuelve de la url de supermanager.acb.com  
            donde se ve la lista de Jugadores que ocupan la posicion.
            
            Las posiciones son: 'base','alero' y 'pivot'"""
        indexposicion = acceso.enumPosiciones.__getattribute__(posicion).Value
        return 'http://supermanager.acb.com/vermercado.php?id_pos=' \
                        + str(indexposicion+1)
    

