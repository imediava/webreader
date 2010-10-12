from webreader.modelos.decoradores import TablaHtml
from webreader.modelos.decoradores import CampoTablaHtml

class Jugador(object):
    
    @CampoTablaHtml(columna=4,ruta_adicional='/a/font')
    def nombre(self):
        pass
    
    @CampoTablaHtml(columna=4,ruta_adicional='/a/@href')
    def website(self):
        pass
    
    @CampoTablaHtml(columna=11,decimal=True)
    def val_jornada(self):
        pass
    
    @CampoTablaHtml(columna=12,decimal=True)
    def val_ultimas3(self):
        pass
    
    @CampoTablaHtml(columna=13,decimal=True)
    def subir15(self):
        pass
    
    @CampoTablaHtml(columna=9,tratar_valor=lambda valor: int(valor.replace(".","")))
    def precio(self):
        pass
    
    @CampoTablaHtml(columna=8,decimal=True)
    def val_media(self):
        pass
    
    @CampoTablaHtml(columna=6)
    def equipo(self):
        pass
    
    posicion = ""

    def __str__(self):
        "Jugador:%s" % self.nombre
        
