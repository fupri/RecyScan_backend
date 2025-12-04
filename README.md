# RecyScan_backEnd

RecyScan es una app móbil que pide una foto de un residuo al usuario y ésta le indica al usuario qué tipo de residuo es, la probabilidad de que lo sea, el contenedor al que debe tirarlo para su debido reciclaje y una breve instrucción para facilitar el reciclaje.

Instrucciones de uso:

1. Abrir un terminal en la raíz del repositorio
2. Ejecutar el comando "pip install -r requirements.txt" para instalar las librerias necesarias
3. Ejecutar el comando "flask --app app run --host=0.0.0.0 --port=5000" para poner en marcha el backend en el puerto de red local del dispositivo

Entrenamiento de la IA:

1. Ir al link del dataset y descargarlo, poniendolo en la misma carpeta que el resto de archivos --> [link del drive]
2. Una vez descargado, descomprimir el archivo.
3. Abrir y ejecutar "training_ia.py" y esperar (puede tardar un tiempo).
