# API con Flask para proyecto de residuos
import os
from Proyecto.backend.Foto import Foto
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
from ClasificadorDAO import ClasificadorResiduosDAO

app = Flask(__name__)

dao = ClasificadorResiduosDAO(model_path = '.\Proyecto\model\modelo_reciclaje.tflite'#, labels_path =
)

# Cargar el modelo preentrenado
print("Cargando modelo...")
model = tf.keras.models.load_model('modelo_residuos.h5')
print("Modelo cargado.")

class_names = ['Cartón', 'Plástico', 'Vidrio', 'Papel', 'Metal', 'Orgánico', 'Otro']
print(f"Clases definidas: {class_names}")

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        file = request.files['file']
        mi_foto = Foto(file_source = file, filename = file.filename)
        categoria_resultado = dao.predecir_imagen(mi_foto)
        return jsonify(categoria_resultado.to_dict())

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories': class_names})

@app.route('/health', methods=['GET'])
def health_check():
    """Comprueba que el servicio está funcionando correctamente."""
    try:
        model_loaded = model is not None
        return jsonify({
        'status': 'ok',
        'model_loaded': model}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/info/<string:category_name>', methods=['GET'])
def get_category_info(category_name):
    recycling_info = {
        'Cartón': {
            'description': 'Material hecho de fibras de celulosa, utilizado para embalajes y envases.',
            'recycling_instructions': 'Plega las cajas limpias y colócalas en el contenedor azul.',
            'common_items': ['Cajas de embalaje', 'Cajas de cereales', 'Tubos de papel higiénico']
        },
        'Plástico': {
            'description': 'Material sintético derivado del petróleo, utilizado en envases y productos desechables.',
            'recycling_instructions': 'Enjuaga los envases y colócalos en el contenedor amarillo.',
            'common_items': ['Botellas de agua', 'Envases de yogur', 'Bolsas de plástico']
        },
        'Vidrio': {
            'description': 'Material inorgánico y transparente, utilizado en botellas y frascos.',
            'recycling_instructions': 'Coloca las botellas y frascos en el contenedor verde, sin tapones.',
            'common_items': ['Botellas de vidrio', 'Frascos de alimentos', 'Vasos rotos']
        },
        'Papel': {
            'description': 'Material hecho de fibras vegetales, utilizado en impresiones y embalajes.',
            'recycling_instructions': 'Coloca el papel limpio en el contenedor azul, sin grapas ni plásticos.',
            'common_items': ['Periódicos', 'Revistas', 'Hojas de papel']
        },
        'Metal': {
            'description': 'Material sólido y maleable, utilizado en latas y utensilios.',
            'recycling_instructions': 'Enjuaga las latas y colócalas en el contenedor amarillo.',
            'common_items': ['Latas de refrescos', 'Utensilios de cocina', 'Aluminio de alimentos']
        },
        'Orgánico': {
            'description': 'Residuos biodegradables provenientes de alimentos y jardinería.',
            'recycling_instructions': 'Coloca los residuos orgánicos en el contenedor marrón o compostaje.',
            'common_items': ['Restos de comida', 'Cáscaras de frutas', 'Residuos de jardín']
        },
        'Otro': {
            'description': 'Residuos que no encajan en las otras categorías.',
            'recycling_instructions': 'Consulta las normativas locales para la disposición adecuada. Generalmente pueden desecharse en el contenedor de resto.',
            'common_items': ['Pañales', 'Cerámicas', 'Objetos contaminados']
        }
    }

    info = recycling_info.get(category_name)
    if info:
        return jsonify(info)
    else:
        return jsonify({'error': 'Categoría no encontrada'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #¡¡¡¡CAMBIAR DEBUG A FALSE EN PRODUCCION!!!!