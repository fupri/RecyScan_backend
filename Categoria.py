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
        'instruccion': 'Plegar cajas',
        'nombre': 'Cartón'
    },
    'plastic': {  # Plástico
        'contenedor': 'Amarillo',
        'instruccion': 'Aplastar botellas',
        'nombre': 'Plásticos y envases'
    },
    'glass': {  # Vidrio
        'contenedor': 'Verde',
        'instruccion': 'Sin tapones ni tapas',
        'nombre': 'Vidrio'
    },
    'paper': {  # Papel
        'contenedor': 'Azul',
        'instruccion': 'Sin grapas',
        'nombre': 'Papel'
    },
    'metal': {  # Metal
        'contenedor': 'Amarillo',
        'instruccion': 'Latas limpias',
        'nombre': 'Metales y latas'
    },
    'organic': {  # Orgánico
        'contenedor': 'Marrón',
        'instruccion': 'Restos de comida',
        'nombre': 'Residuos orgánicos'
    },
    'clothes': {  # Textil
        'contenedor': 'Naranja',
        'instruccion': 'Ropa usada',
        'nombre': 'Ropa y textiles'
    },
    'shoes': {  # Calzado
        'contenedor': 'Naranja',
        'instruccion': 'Calzado usado',
        'nombre': 'Calzado'
    },
    'vegetation': {  # Vegetación
        'contenedor': 'Marrón',
        'instruccion': 'Residuos de jardín',
        'nombre': 'Residuos de jardinería'
    },
    'miscellaneous': {  # Otro
        'contenedor': 'Gris/Punto Limpio',
        'instruccion': 'Consultar normativa',
        'nombre': 'Otros residuos'
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
            "instruccion": self.metadata['instruccion'],
            "nombre": self.metadata['nombre'],
        }