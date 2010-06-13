class Jugador(object):

    nombre = ""
    val_media = ""
    val_jornada = ""
    val_ultimas3 = ""
    subir15 = ""
    precio = ""
    website = ""
    posicion = ""
    equipo = ""

    def __str__(self):
        "Jugador:%s" % self.nombre
