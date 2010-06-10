from webreader.extraccion.acceso import enumPosiciones
from webreader.extraccion.ParsersWeb import ParserJugadores

def actualizar_tabla():
    import time
    print "Empezando: %s" % (time.ctime())
    for posicion in enumPosiciones:
        parser = ParserJugadores(str(posicion))
    	print "Parseados Jugadores(%s): %s" % (str(posicion),time.ctime())
        #fachada.guardarlista(parser.parsearlista())
	print parser.parsearlista()
	print "Guardados Jugadores(%s): %s" % (str(posicion),time.ctime())


if __name__ == "__main__":
	actualizar_tabla()




    
    

