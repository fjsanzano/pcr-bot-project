# Proyecto PCR Bot 
Simple Telegram bot para publicar los resultados de las Pruebas PCR

El bot se debe instalar en un servidor donde tenga acceso a la base de datos del sistema y a su ves a los servidores de Telegram.
Instalar las dependencias utilizando el comando 'pip install -r requirements.txt'

Configurar los parametros de la base de datos en el "config.py" como por ejemplo
hostname = 'localhost'
username = 'root'
password = 'root123'
database = 'cordinacion'

Se debe configurar el TOKEN del bot de telegram en el "config.py", esto debe ser secreto ya que le da los privilegios de administrar el bot

Despues correr el script y buscar el bot en Telegram para probar.

Se recomienda hacer un servicio con el script en caso de que se detenga el servidor inicie solo.