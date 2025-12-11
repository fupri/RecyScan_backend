class Categoria:
    
    __recycling_info = {
    'battery': {
        'description': 'Dispositivos portátiles que almacenan energía química para su uso en aparatos electrónicos.',
        'container': 'Lleva las baterías usadas a puntos de recogida específicos o tiendas autorizadas.',
        'common_items': ['Baterías AA', 'Baterías de teléfonos móviles', 'Baterías de portátiles']
    },
    'cardboard': {
        'description': 'Material hecho de fibras de celulosa, utilizado para embalajes y envases.',
        'container': 'Plega las cajas limpias y colócalas en el contenedor azul.',
        'common_items': ['Cajas de embalaje', 'Cajas de cereales', 'Tubos de papel higiénico']
    },
    'clothes': {
        'description': 'Material hecho de fibras naturales o sintéticas, utilizado en ropa y accesorios.',
        'container': 'Deposita la ropa usada en contenedores específicos para textiles.',
        'common_items': ['Ropa vieja', 'Zapatos usados', 'Sábanas y toallas']
    },
    'glass': {
        'description': 'Material inorgánico y transparente, utilizado en botellas y frascos.',
        'container': 'Coloca las botellas y frascos en el contenedor verde, sin tapones.',
        'common_items': ['Botellas de vidrio', 'Frascos de alimentos', 'Vasos rotos']
    },
    'metal': {
        'description': 'Material sólido y maleable, utilizado en latas y utensilios.',
        'container': 'Enjuaga las latas y colócalas en el contenedor amarillo.',
        'common_items': ['Latas de refrescos', 'Utensilios de cocina', 'Aluminio de alimentos']
    },
    'miscellaneous': {
        'description': 'Residuos que no encajan en las otras categorías.',
        'container': 'Consulta las normativas locales para la disposición adecuada. Generalmente pueden desecharse en el contenedor de resto.',
        'common_items': ['Pañales', 'Cerámicas', 'Objetos contaminados']
    },
    'organic': {
        'description': 'Residuos biodegradables provenientes de alimentos y jardinería.',
        'container': 'Coloca los residuos orgánicos en el contenedor marrón o compostaje.',
        'common_items': ['Restos de comida', 'Cáscaras de frutas', 'Residuos de jardín']
    },
    'paper': {
        'description': 'Material hecho de fibras vegetales, utilizado en impresiones y embalajes.',
        'container': 'Coloca el papel limpio en el contenedor azul, sin grapas ni plásticos.',
        'common_items': ['Periódicos', 'Revistas', 'Hojas de papel']
    },
    'plastic': {
        'description': 'Material sintético derivado del petróleo, utilizado en envases y productos desechables.',
        'container': 'Enjuaga los envases y colócalos en el contenedor amarillo.',
        'common_items': ['Botellas de agua', 'Envases de yogur', 'Bolsas de plástico']
    },
    'shoes': {
        'description': 'Material utilizado para fabricar zapatos y botas.',
        'container': 'Deposita los zapatos usados en contenedores específicos para calzado.',
        'common_items': ['Zapatos deportivos', 'Botas', 'Sandalias']
    },
    'vegetation': {
        'description': 'Residuos biodegradables provenientes de plantas y jardines.',
        'container': 'Coloca los residuos vegetales en el contenedor marrón o compostaje.',
        'common_items': ['Hojas', 'Ramas', 'Restos de jardín']
    },
}

    def __init__(self, nombre, confianza, indice):
        self.nombre = nombre
        self.confianza = confianza
        self.indice = indice
        self.metadata = self.cargar_metadata() # Auto-enriquecimiento

    
    @classmethod
    def get_recycling_info(cls):
        return cls.__recycling_info

    def cargar_metadata(self):
        # Cada categoría sabe su propia información de reciclaje.
        print(f"Cargando metadata para categoría: {self.nombre}")
        # Usar el diccionario compartido `recycling_info` definido a nivel de módulo
        return self.__recycling_info.get(self.nombre, {'container': 'Desconocido', 'description': 'N/A', 'common_items': []})

    def to_dict(self):
        """Helper para convertir el objeto a JSON para la API"""
        return {
            "categoria": self.nombre,
            "confianza": self.confianza,
            "contenedor": self.metadata['container'],
            "descripcion": self.metadata['description'],
            "objetos_comunes": self.metadata['common_items'],
        }