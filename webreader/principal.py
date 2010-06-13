#!/usr/bin/python
# -*- coding: latin-1 -*-

from webreader.extraccion.acceso import enumPosiciones
from webreader.extraccion.ParsersWeb import ParserJugadores

import locale
#Asigna como local el es_UTF8
#locale.setlocale(locale.LC_ALL,'')

def actualizar_tabla():
    import time
    print "Empezando: %s" % (time.ctime())
    for posicion in enumPosiciones:
	url = getUrlPosicion(str(posicion))
        parser = ParserJugadores()
    	print "Comienzo parseado de (%s): %s" % (str(posicion),time.ctime())
        #fachada.guardarlista(parser.parsearlista())
	lista = parser.parsearlista(url)
        print lista[0].nombre
	
	print "Guardados Jugadores(%s): %s" % (str(posicion),time.ctime())
	
    exportarcsv(lista)

def exportarcsv(lista):
    from csv import DictWriter
    f = open('/home/imediava/Escritorio/salvar.csv', 'wt')
    writer = DictWriter(f,lista[0].__dict__.keys())
    titulos = {}
    for elem in lista[0].__dict__.keys():
	titulos[elem] = elem
	
    writer.writerow(titulos)
    import codecs
    for elem in lista:
	#nombre_unicode = unicode(elem.nombre, 'latin1') # Unicode string
        elem.nombre = elem.nombre.encode('utf8')  # UTF-8 byte string
	writer.writerow(elem.__dict__)
    f.close()
    
def getUrlPosicion(posicion):
        """Devuelve de la url de supermanager.acb.com  
            donde se ve la lista de Jugadores que ocupan la posicion.
            
            Las posiciones son: 'base','alero' y 'pivot'"""
        indexposicion = enumPosiciones.__getattribute__(posicion).Value
        return 'http://supermanager.acb.com/vermercado.php?id_pos=' \
                        + str(indexposicion+1)



if __name__ == "__main__":
	actualizar_tabla()




    
    

