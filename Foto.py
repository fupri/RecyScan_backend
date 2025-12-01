class Foto:
    """
    ### CAMBIO: Nueva clase para encapsular la imagen.
    Abstrae el origen de la imagen (path local o archivo subido por API).
    """
    def __init__(self, file_source, filename=None):
        self.__file_source = file_source
        self.__filename = filename or "unknown.jpg"

    def get_image_stream(self):
        """Devuelve el objeto imagen listo para ser abierto por PIL"""
        return self.__file_source