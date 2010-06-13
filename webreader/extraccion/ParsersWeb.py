from StringIO import StringIO
from webreader.modelos.jugador import Jugador
import acceso
from LectorXPath import LectorTablasHtmlXPath,LectorTablasHtmlXPath,toBeautifulSoup
from LectorXPath import CampoCeldaTablaHTML
from LectorXPath import TablaHTML
from abc import ABCMeta, abstractmethod,abstractproperty

class ParserHtml:
    
    __metaclass__ = ABCMeta
    
    """ Contiene metodos comunes para tratar el acceso a web """
    
    def __init__(self):
	self.acceso_conex = acceso.AccesoHTTPSupermanager()
	
   
    def parsearlista(self,url):
	self.cadena = self.acceso_conex.obtenerFicheroPagina(url)
        self.lectorXPath = LectorTablasHtmlXPath(self.tabla.ruta_xpath,self.cadena)
        lista = []
	fila_fin = len(self.lectorXPath.obtener_todos(self.tabla.ruta_xpath,'tr'))
	for num_fila in range(self.tabla.fila_inicio,fila_fin):
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
	pass
    
    
    @abstractproperty
    def tabla(self):
	pass
    
    @abstractproperty
    def clase_modelo(self):
	pass
    
    @abstractproperty
    def campos(self):
	pass
    
 

class ParserJugadores(ParserHtml):
    
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

    
    
    

