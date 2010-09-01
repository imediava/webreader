from StringIO import StringIO
from webreader.modelos.jugador import Jugador
from webreader.modelos.estadisticas_jugador_partido import Estadisticas_jugador_partido
import acceso
from LectorXPath import LectorTablasHtmlXPath,LectorTablasHtmlXPath,toBeautifulSoup
from LectorXPath import CampoCeldaTablaHTML
from LectorXPath import TablaHTML
from abc import ABCMeta, abstractmethod,abstractproperty



class ParserTablaHtml(object):
    """ Clase abstracta que tienen que implementar todos los
    parsers que quieran leer informacion de una tabla HTML."""
    
    __metaclass__ = ABCMeta
    
    def __init__(self):
	""" Inicia una conexion HTTP."""
	self.acceso_conex = acceso.AccesoHTTP()
	
   
    def parsearlista(self,url):
	""" Recibe una url y parsea la tabla devolviendo una lista de las filas leidas.
	
	Los parametros son las propiedades de el parser:
	- Tabla: informacion de como localizar y tratar la tabla.
	- Campos: campos a leer de la tabla.
	- Modelo: clase de python donde se guardaran los datos leidos en una fila."""
	
	self.cadena = self.acceso_conex.obtenerFicheroPagina(url)
        self.lectorXPath = LectorTablasHtmlXPath(self.tabla.ruta_xpath,self.cadena)
        lista = []
	fila_fin = len(self.lectorXPath.obtener_todos(self.tabla.ruta_xpath,'tr'))
	ultima_fila_a_leer = fila_fin - self.tabla.filas_sin_leer_al_final
	for num_fila in range(self.tabla.fila_inicio,ultima_fila_a_leer):
	    # Creo un elemento del tipo modelo que es un objeto de tipo Class
	    # si modelo es la clase Jugador es como decir: elemento = Jugador()
	    elemento = self.clase_modelo()
	    for nombrecampo,campo in self.campos.items():
		valor_original = self.lectorXPath.leer_campo(num_fila,campo)
		valor = self.tratar_valor(nombrecampo,valor_original)
		elemento.__setattr__(nombrecampo,valor)
	    lista.append(elemento)
                
        return lista
    
    @abstractmethod
    def tratar_valor(nombrecampo,valor_original):
	""" Permite modificar el valor de un campo que se lee de la tabla html."""
	pass
    
    
    @abstractproperty
    def tabla(self):
	""" Objecto con informacion de la tabla a leer.
	
	Ver :py:class:`webreader.extraccion.LectorXPath.TablaHTML` para mas informacion
	sobre los campos necesarios para describir la tabla."""
	pass
    
    @abstractproperty
    def clase_modelo(self):
	""" Clase que define los objetos que van a formar la lista que devuelve parsearlista.
	
	La clase tiene que tener al menos como variables publicas la misma lista de campos
	que los definidos en :py:attribute::`campos`
	"""
	pass
    
    @abstractproperty
    def campos(self):
	pass
    
 
class ParserTablaHtmlACB(ParserTablaHtml):
    
    __metaclass__ = ABCMeta
	
    def __init__(self):
	    self.acceso_conex = acceso.AccesoHTTPSupermanager()
      
class ParserJugadores(ParserTablaHtmlACB):
    
    _tabla = TablaHTML(ruta_xpath = '/html/body/table[2]/tbody/tr/td[3]/table[2]/tbody',
		      fila_inicio=3,filas_sin_leer_al_final=0)
    
    @property
    def tabla(self):
	return self._tabla
    
    
    _modelo = Jugador
    
    @property
    def clase_modelo(self):
	return self._modelo
    
    _campos = {
	'nombre' : CampoCeldaTablaHTML(columna=4,ruta_adicional='/a/font') ,
	'website' : CampoCeldaTablaHTML(columna=4,ruta_adicional='/a/@href') ,
	'val_jornada' : CampoCeldaTablaHTML(columna=11,decimal=True) ,
	'val_ultimas3' : CampoCeldaTablaHTML(columna=12,decimal=True) ,
	'subir15' : CampoCeldaTablaHTML(columna=13,decimal=True) ,
	'precio' : CampoCeldaTablaHTML(columna=9) ,
	'val_media' : CampoCeldaTablaHTML(columna=8,decimal=True) ,
	'equipo' : CampoCeldaTablaHTML(columna=6)
    }
    
    @property
    def campos(self):
	return self._campos
    
    def tratar_valor(self,nombrecampo,valor_original):
	if nombrecampo == 'precio':
	    return int(valor_original.replace(".",""))
	return valor_original
    
    
class ParserPartidosJugador(ParserTablaHtml):
    
    _tabla = TablaHTML(ruta_xpath = '/html/body/table/tbody/tr[2]/td/table[3]',
    fila_inicio = 3, filas_sin_leer_al_final = 2)
    
    @property
    def tabla(self):
	return self._tabla

    _modelo = Estadisticas_jugador_partido
    
    @property
    def clase_modelo(self):
	return self._modelo
    
    _campos = {
	'equipos' : CampoCeldaTablaHTML(columna=3,ruta_adicional='/a') ,
	'minutos_jugados' : CampoCeldaTablaHTML(columna=4) ,
	'puntos' : CampoCeldaTablaHTML(columna=5) ,
	'tiros_de_dos' : CampoCeldaTablaHTML(columna=6) ,
	'tiros_de_tres' : CampoCeldaTablaHTML(columna=7) ,
	'tiros_libres' : CampoCeldaTablaHTML(columna=8) ,
	'rebotes' : CampoCeldaTablaHTML(columna=9) ,
	'asistencias' : CampoCeldaTablaHTML(columna=10) ,
	'balones_recuperados' : CampoCeldaTablaHTML(columna=11) ,
	'balones_perdidos' : CampoCeldaTablaHTML(columna=12) ,
	'valoracion' : CampoCeldaTablaHTML(columna=18)
    }
    
    @property
    def campos(self):
	return self._campos
    
    def tratar_valor(self,nombrecampo,valor_original):
	return valor_original

