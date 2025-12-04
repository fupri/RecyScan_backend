import zipfile
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import zipfile
import shutil

# CONFIGURACIÓN DEL DATASET

dataset_folder = "datasets"

img_height = 224  # tamaño recomendado para MobileNetV2
img_width = 224
batch_size = 32
seed = 123

# Ordenar clases para reproducibilidad
class_names_fixed = sorted([d for d in os.listdir(dataset_folder) if os.path.isdir(os.path.join(dataset_folder, d))])
print("CLASES DETECTADAS:", class_names_fixed)

train_ds = keras.preprocessing.image_dataset_from_directory(
    dataset_folder,
    validation_split=0.2,
    subset="training",
    seed=seed,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    shuffle=True,
    class_names=class_names_fixed
)

val_ds = keras.preprocessing.image_dataset_from_directory(
    dataset_folder,
    validation_split=0.2,
    subset="validation",
    seed=seed,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    shuffle=True,
    class_names=class_names_fixed
)

# Normalización (0-1)
train_ds = train_ds.map(lambda x, y: (x / 255.0, y))
val_ds = val_ds.map(lambda x, y: (x / 255.0, y))

# data augmentation

data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
    layers.RandomContrast(0.1)
])


# transfer learning MobileNetV2

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(img_height, img_width, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = True  # congelar pesos preentrenados
for layer in base_model.layers[:100]:
    layer.trainable = False

# Construir modelo completo
model = keras.Sequential([
    layers.Input(shape=(img_height, img_width, 3)),
    data_augmentation,
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(len(class_names_fixed), activation='softmax')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.00001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# entranar el modelo

model.fit(train_ds, validation_data=val_ds, epochs=10)

# Guardar modelo
model.save("modelo_reciclaje.h5")
print("\nModelo guardado como modelo_reciclaje.h5\n")

# Cargar el modelo entrenado
model = tf.keras.models.load_model("modelo_reciclaje.h5")

# Convertir a TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Guardar el modelo TFLite
with open("modelo_reciclaje.tflite", "wb") as f:
    f.write(tflite_model)

print("Modelo convertido a TFLite listo para móvil.")