class Foto:
    """
    ### CAMBIO: Nueva clase para encapsular la imagen.
    Abstrae el origen de la imagen (path local o archivo subido por API).
    """
    def __init__(self, file_source, filename=None):
        self.file_source = file_source
        self.filename = filename or "unknown.jpg"

    def get_image_stream(self):
        """Devuelve el objeto imagen listo para ser abierto por PIL"""
        return self.file_source