class Categoria:
    """
    Ya no es un diccionario simple, es un objeto con propiedades y lógica.
    """
    def __init__(self, nombre, confianza, indice):
        self.nombre = nombre
        self.confianza = confianza
        self.indice = indice
        self.metadata = self._cargar_metadata() # Auto-enriquecimiento

    def _cargar_metadata(self):
        """
        Cada categoría sabe su propia información de reciclaje.
        """
        info_db = {
    'cardboard': {  # Cartón
        'contenedor': 'Azul',
        'instruccion': 'Plegar cajas'
    },
    'plastic': {  # Plástico
        'contenedor': 'Amarillo',
        'instruccion': 'Aplastar botellas'
    },
    'glass': {  # Vidrio
        'contenedor': 'Verde',
        'instruccion': 'Sin tapones ni tapas'
    },
    'paper': {  # Papel
        'contenedor': 'Azul',
        'instruccion': 'Sin grapas'
    },
    'metal': {  # Metal
        'contenedor': 'Amarillo',
        'instruccion': 'Latas limpias'
    },
    'organic': {  # Orgánico
        'contenedor': 'Marrón',
        'instruccion': 'Restos de comida'
    },
    'clothes': {  # Textil
        'contenedor': 'Naranja',
        'instruccion': 'Ropa usada'
    },
    'shoes': {  # Calzado
        'contenedor': 'Naranja',
        'instruccion': 'Calzado usado'
    },
    'vegetation': {  # Vegetación
        'contenedor': 'Marrón',
        'instruccion': 'Residuos de jardín'
    },
    'miscellaneous': {  # Otro
        'contenedor': 'Gris/Punto Limpio',
        'instruccion': 'Consultar normativa'
    }
        }
        print(f"Cargando metadata para categoría: {self.nombre}")
        return info_db.get(self.nombre, {'contenedor': 'Desconocido', 'instruccion': 'N/A'})

    def to_dict(self):
        """Helper para convertir el objeto a JSON para la API"""
        return {
            "categoria": self.nombre,
            "confianza": self.confianza,
            "contenedor": self.metadata['contenedor'],
            "instruccion": self.metadata['instruccion']
        }