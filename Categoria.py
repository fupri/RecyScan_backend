class Categoria:
    """
    Ya no es un diccionario simple, es un objeto con propiedades y lógica.
    """
    def __init__(self, nombre, confianza, indice):
        self.__nombre = nombre
        self.__confianza = confianza
        self.__indice = indice
        self.__metadata = self._cargar_metadata() # Auto-enriquecimiento

    def _cargar_metadata(self):
        """
        Cada categoría sabe su propia información de reciclaje.
        """
        info_db = {
            'Cartón': {'contenedor': 'Azul', 'instruccion': 'Plegar cajas'},
            'Plástico': {'contenedor': 'Amarillo', 'instruccion': 'Aplastar botellas'},
            'Vidrio': {'contenedor': 'Verde', 'instruccion': 'Sin tapones ni tapas'},
            'Papel': {'contenedor': 'Azul', 'instruccion': 'Sin grapas'},
            'Metal': {'contenedor': 'Amarillo', 'instruccion': 'Latas limpias'},
            'Orgánico': {'contenedor': 'Marrón', 'instruccion': 'Restos de comida'},
            'Textil': {'contenedor': 'Naranja', 'instruccion': 'Ropa usada'},
            'Vegetación': {'contenedor': 'Marrón', 'instruccion': 'Residuos de jardín'},
            'Otro': {'contenedor': 'Gris/Punto Limpio', 'instruccion': 'Consultar normativa'}
        }
        return info_db.get(self.__nombre, {'contenedor': 'Desconocido', 'instruccion': 'N/A'})

    def to_dict(self):
        """Helper para convertir el objeto a JSON para la API"""
        return {
            "categoria": self.__nombre,
            "confianza": self.__confianza,
            "contenedor": self.__metadata['contenedor'],
            "instruccion": self.__metadata['instruccion']
        }