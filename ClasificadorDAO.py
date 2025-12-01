import tensorflow as tf
import numpy as np
from PIL import Image
import os
from datetime import datetime
from Foto import Foto
from Categoria import Categoria

class ClasificadorResiduosDAO:
    def __init__(self, model_path, labels_path=None):
        self.model_path = model_path
        
        # Cargar TFLite
        try:
            self.interpreter = tf.lite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.input_shape = self.input_details[0]['shape']
            self.height = self.input_shape[1]
            self.width = self.input_shape[2]
            print(f"DAO Iniciado. Modelo TFLite cargado.")
        except Exception as e:
            raise e

        # Cargar etiquetas
        if labels_path and os.path.exists(labels_path):
            with open(labels_path, 'r') as f:
                self.class_names = [line.strip() for line in f.readlines()]
        else:
            self.class_names = ['Cartón', 'Plástico', 'Vidrio', 'Papel', 'Metal', 'Orgánico', 'Textil', 'Vegetación', 'Otro']

    def _generar_matriz_input(self, foto: Foto):
        """
        Convierte el objeto Foto en la matriz numérica para el modelo.
        """
        # Usamos el método de la clase Foto para obtener el stream
        img = Image.open(foto.get_image_stream()).convert('RGB')
        
        img = img.resize((self.width, self.height))
        input_data = np.array(img, dtype=np.float32)
        input_data = input_data / 255.0 # Normalización
        input_data = np.expand_dims(input_data, axis=0)
        
        return input_data

    def predecir_imagen(self, foto: Foto) -> Categoria:
        """
        Función principal.
        Entrada: Objeto Foto
        Salida: Objeto Categoria
        """
        # 1. Procesar Foto
        input_data = self._generar_matriz_input(foto)
        
        # 2. Inferencia TFLite
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        
        # 3. Procesar resultados
        predictions = output_data[0]
        predicted_index = np.argmax(predictions)
        confidence = float(np.max(predictions))
        predicted_name = self.class_names[predicted_index]
        
        # 4. Instanciamos y devolvemos un objeto de dominio
        categoria_detectada = Categoria(
            nombre=predicted_name, 
            confianza=confidence,
            indice=int(predicted_index)
        )
        
        return categoria_detectada

    # =========================================================================
    #  MÉTODOS FUTUROS (Aún no conectados a la API)
    # =========================================================================

    def obtener_top_k(self, foto: Foto, k=3) -> list[Categoria]:
        """
        Útil para cuando la IA duda: 'No sé si es Vidrio o Plástico'.
        """
        input_data = self._generar_matriz_input(foto)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])[0]

        top_k_indices = output_data.argsort()[-k:][::-1]
        
        resultados = []
        for idx in top_k_indices:
            # Creamos objetos Categoria para cada posibilidad
            cat = Categoria(
                nombre=self.class_names[idx], 
                confianza=float(output_data[idx]),
                indice=int(idx)
            )
            resultados.append(cat)
            
        return resultados

    def guardar_feedback(self, foto: Foto, categoria_real: Categoria):
        """
        Guarda la foto en una carpeta para re-entrenar luego.
        """
        base_folder = "dataset_feedback"
        save_path = os.path.join(base_folder, categoria_real.nombre)
        os.makedirs(save_path, exist_ok=True)
        
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{foto.filename}"
        
        img = Image.open(foto.get_image_stream())
        img.save(os.path.join(save_path, filename))
        print(f"Feedback guardado: {filename} es realmente {categoria_real.nombre}")