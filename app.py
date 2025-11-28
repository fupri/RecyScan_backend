#API con Flask para proyecto de residuos
import os
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

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

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Preprocesar la imagen
        img = Image.open(file).convert('RGB')
        img = img.resize((200, 200))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        # Hacer la predicción
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        # Obtener la clase con mayor probabilidad
        predicted_class_index = class_names[np.argmax(predictions[0])]
        predicted_class_name = class_names[predicted_class_index]
        confidence = float(np.max(predictions[0]))
        print(f"Predicción: {predicted_class_name} con confianza {confidence:.4f}")

        return jsonify({
            "object": predicted_class_name,
            "category": predicted_class_name,
            "confidence": confidence
        })
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #¡¡¡¡CAMBIAR DEBUG A FALSE EN PRODUCCION!!!!