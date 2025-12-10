# API con Flask para proyecto de residuos
import os
from Foto import Foto
from flask import Flask, request, jsonify
from Clasificador_main import ClasificadorResiduos
from datetime import datetime
from Categoria import Categoria

app = Flask(__name__)

predictor = ClasificadorResiduos(model_path = os.path.join('model', 'modelo_reciclaje_0.92accurate.tflite'))

print(f"Clases definidas: {list(Categoria.get_recycling_info().keys())}")

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        mi_foto = Foto(file_source = file, filename = file.filename)
        categoria_resultado = predictor.predecir_imagen(mi_foto)
        # Si la confianza es baja (< 0.8), devolvemos las dos mejores predicciones
        try:
            confianza = float(categoria_resultado.confianza)
        except Exception:
            confianza = None

        if confianza is not None and confianza < 0.8:
            top2 = predictor.obtener_top_k(mi_foto, k=2)
            return jsonify({
                'Predicciones': [c.to_dict() for c in top2],
                'Nota': 'Confianza baja - devolviendo las 2 mejores predicciones'
            })

        return jsonify(categoria_resultado.to_dict())

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Comprueba que el servicio web responde Y que el modelo de IA funciona.
    """
    try:
        # Le preguntamos al predictor si el cerebro (TFLite) funciona
        ai_is_ready = predictor.health_check_model()

        if ai_is_ready:
            return jsonify({
                'status': 'online',
                'service': 'GarbageClassifier API',
                'model_status': 'ready',
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            # El servidor web va, pero la IA falló
            return jsonify({
                'status': 'degraded',
                'model_status': 'failed',
                'message': 'El modelo no responde a la prueba de inferencia.'
            }), 503

    except Exception as e:
        return jsonify({
            'status': 'error', 
            'message': f"Error interno: {str(e)}"
        }), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories': list(Categoria.get_recycling_info().keys())}), 200

@app.route('/categories/<string:category_name>', methods=['GET'])
def get_category_info(category_name):
    info = Categoria.get_recycling_info().get(category_name)
    if info:
        return jsonify({
            'status': 'success',
            'category': category_name,
            'data': info
        }), 200
    else:
        return jsonify({'error': 'Categoría no encontrada'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #¡¡¡¡CAMBIAR DEBUG A FALSE EN PRODUCCION!!!!