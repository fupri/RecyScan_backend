# RecyScan_backEnd

RecyScan es una app móvil creada para facilitar el reciclaje. Entrenada con múltiples datasets, la inteligencia artificial es capaz de identificar residuos con un 0.92% de acierto en pruebas controladas. Una vez que se abre la app, esta pide al usuario una imagen del residuo o residuos que se desean reciclar. Esta imagen se compara con los datos de la IA para deducir qué contenedor es el idóneo y una breve instrucción para facilitar el reciclaje.

Instrucciones de uso:

1. Abrir un terminal en la raíz del repositorio
2. Ejecutar el comando "uv add requests" para instalar las librerias necesarias
3. Ejecutar el comando "flask --app app run --host=0.0.0.0 --port=5000" para poner en marcha el backend en el puerto de red local del dispositivo

Entrenamiento de la IA:

1. Ir al link del dataset y descargarlo, poniendolo en la misma carpeta que el resto de archivos --> [https://drive.google.com/file/d/1ZhyRWr8eqKWuHSx5rxILLldra6nNg2_C/view?usp=sharing]
2. Una vez descargado, descomprimir el archivo.
3. Abrir y ejecutar "training_ia.py" y esperar (puede tardar un tiempo).
