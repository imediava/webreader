from StringIO import StringIO
from webreader.modelos.jugador import Jugador
from webreader.modelos.estadisticas_jugador_partido import Estadisticas_jugador_partido
import acceso
from LectorXPath import LectorTablasHtmlXPath,LectorTablasHtmlXPath,toBeautifulSoup
from LectorXPath import ModeloColumnaTablaHTML
from LectorXPath import ModeloTablaHTML
from abc import ABCMeta, abstractmethod,abstractproperty



class ParserHtml:
    
    __metaclass__ = ABCMeta
    
    def __init__(self,lector_tablas):
	self.lector_tablas = lector_tablas
    
    """ Contiene metodos comunes para tratar el acceso a web """
    
    def parsearlista(self,html_content,table_model):
	""" Returns a list of objects of the table_model. """
        tabla = self.lector_tablas(table_model,html_content).obtener_tabla()
        lista = []
	# Ahora se recorre las filas de la tabla
	for fila in tabla.get_all_rows():
	    # Creo un elemento del tipo modelo que es un objeto de tipo Class
	    # si modelo es la clase Jugador es como decir: elemento = Jugador()
	    elemento = self.clase_modelo()
	    for nombre_campo,valor in fila.items():
		elemento.__setattr__(nombre_campo,valor)
	    lista.append(elemento)
                
        return lista
    
    
    @abstractproperty
    def modelo_tabla(self):
	pass
    
    @abstractproperty
    def clase_modelo(self):
	pass
    

class ParserJugadores(ParserHtml):
    
    _campos = [
	ModeloColumnaTablaHTML(nombre='nombre',columna=4,ruta_adicional='/a/font') ,
	ModeloColumnaTablaHTML(nombre='website',columna=4,ruta_adicional='/a/@href') ,
	ModeloColumnaTablaHTML(nombre='val_jornada',columna=11,decimal=True) ,
	ModeloColumnaTablaHTML(nombre='val_ultimas3',columna=12,decimal=True) ,
	ModeloColumnaTablaHTML(nombre='subir15',columna=13,decimal=True) ,
	ModeloColumnaTablaHTML(nombre='precio',columna=9,
			    tratar_valor=lambda valor: int(valor.replace(".",""))),
	ModeloColumnaTablaHTML(nombre='val_media',columna=8,decimal=True) ,
	ModeloColumnaTablaHTML(nombre='equipo',columna=6)
    ]
    
    
    _tabla = ModeloTablaHTML(campos=_campos,ruta_xpath = '/html/body/table[2]/tbody/tr/td[3]/table[2]/tbody',
		      fila_inicio=3,filas_sin_leer_al_final=0)
    
    @property
    def modelo_tabla(self):
	return self._tabla
    
    
    _modelo = Jugador
    
    @property
    def clase_modelo(self):
	return self._modelo
    
    
class ParserPartidosJugador(ParserHtml):
    
    _campos = [
	ModeloColumnaTablaHTML(nombre='equipos',columna=3,ruta_adicional='/a') ,
	ModeloColumnaTablaHTML(nombre='minutos_jugados',columna=4) ,
	ModeloColumnaTablaHTML(nombre='puntos',columna=5) ,
	ModeloColumnaTablaHTML(nombre='tiros_de_dos',columna=6) ,
	ModeloColumnaTablaHTML(nombre='tiros_de_tres',columna=7) ,
	ModeloColumnaTablaHTML(nombre='tiros_libres',columna=8) ,
	ModeloColumnaTablaHTML(nombre='rebotes',columna=9) ,
	ModeloColumnaTablaHTML(nombre='asistencias',columna=10) ,
	ModeloColumnaTablaHTML(nombre='balones_recuperados',columna=11) ,
	ModeloColumnaTablaHTML(nombre='balones_perdidos',columna=12) ,
	ModeloColumnaTablaHTML(nombre='valoracion',columna=18)
    ]
    
    _tabla = ModeloTablaHTML(campos=_campos,ruta_xpath = '/html/body/table/tbody/tr[2]/td/table[3]',
    fila_inicio = 3, filas_sin_leer_al_final = 2)
    
    @property
    def modelo_tabla(self):
	return self._tabla

    _modelo = Estadisticas_jugador_partido
    
    @property
    def clase_modelo(self):
	return self._modelo
    
