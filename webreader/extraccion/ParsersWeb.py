from StringIO import StringIO
from webreader.modelos.jugador import Jugador
from webreader.modelos.estadisticas_jugador_partido import Estadisticas_jugador_partido
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
	ultima_fila_a_leer = fila_fin - self.tabla.filas_sin_leer_al_final
	# Ahora se recorre las filas desde la inicial a la final ambas incluidas
	for num_fila in range(self.tabla.fila_inicio,ultima_fila_a_leer + 1):
	    # Creo un elemento del tipo modelo que es un objeto de tipo Class
	    # si modelo es la clase Jugador es como decir: elemento = Jugador()
	    elemento = self.clase_modelo()
	    for campo in self.tabla.campos:
		valor_original = self.lectorXPath.leer_campo(num_fila,campo)
		valor = campo.tratar_valor(valor_original)
		elemento.__setattr__(campo.nombre,valor)
	    lista.append(elemento)
                
        return lista
    
    
    @abstractproperty
    def tabla(self):
	pass
    
    @abstractproperty
    def clase_modelo(self):
	pass
    

class ParserJugadores(ParserHtml):
    
    _campos = [
	CampoCeldaTablaHTML(nombre='nombre',columna=4,ruta_adicional='/a/font') ,
	CampoCeldaTablaHTML(nombre='website',columna=4,ruta_adicional='/a/@href') ,
	CampoCeldaTablaHTML(nombre='val_jornada',columna=11,decimal=True) ,
	CampoCeldaTablaHTML(nombre='val_ultimas3',columna=12,decimal=True) ,
	CampoCeldaTablaHTML(nombre='subir15',columna=13,decimal=True) ,
	CampoCeldaTablaHTML(nombre='precio',columna=9,
			    tratar_valor=lambda valor: int(valor.replace(".",""))),
	CampoCeldaTablaHTML(nombre='val_media',columna=8,decimal=True) ,
	CampoCeldaTablaHTML(nombre='equipo',columna=6)
    ]
    
    
    _tabla = TablaHTML(campos=_campos,ruta_xpath = '/html/body/table[2]/tbody/tr/td[3]/table[2]/tbody',
		      fila_inicio=3,filas_sin_leer_al_final=0)
    
    @property
    def tabla(self):
	return self._tabla
    
    
    _modelo = Jugador
    
    @property
    def clase_modelo(self):
	return self._modelo
    
    
class ParserPartidosJugador(ParserHtml):
    
    _campos = [
	CampoCeldaTablaHTML(nombre='equipos',columna=3,ruta_adicional='/a') ,
	CampoCeldaTablaHTML(nombre='minutos_jugados',columna=4) ,
	CampoCeldaTablaHTML(nombre='puntos',columna=5) ,
	CampoCeldaTablaHTML(nombre='tiros_de_dos',columna=6) ,
	CampoCeldaTablaHTML(nombre='tiros_de_tres',columna=7) ,
	CampoCeldaTablaHTML(nombre='tiros_libres',columna=8) ,
	CampoCeldaTablaHTML(nombre='rebotes',columna=9) ,
	CampoCeldaTablaHTML(nombre='asistencias',columna=10) ,
	CampoCeldaTablaHTML(nombre='balones_recuperados',columna=11) ,
	CampoCeldaTablaHTML(nombre='balones_perdidos',columna=12) ,
	CampoCeldaTablaHTML(nombre='valoracion',columna=18)
    ]
    
    _tabla = TablaHTML(campos=_campos,ruta_xpath = '/html/body/table/tbody/tr[2]/td/table[3]',
    fila_inicio = 3, filas_sin_leer_al_final = 2)
    
    @property
    def tabla(self):
	return self._tabla

    _modelo = Estadisticas_jugador_partido
    
    @property
    def clase_modelo(self):
	return self._modelo
    
