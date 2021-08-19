# -*- coding: utf-8 -*-
"""
:copyright: (c) 2021 by Fidel Jimenez Sanzano <fidel.jimenez@uic.cu> or <fidel.jimenez@desoft.cu>
:license: GPLv3, see LICENSE for more details.
"""

# Importamos las librerías de python necesarias
import telebot
import mysql.connector
import re

# Importamos el archivo de configuracion
from config import TOKEN, hostname, username, password, database


# Funcion para buscar los resultados de las pruebas dado un carnet de identidad
# Devuelve los resultados de las ultimas pruebas aplicadas al paciente ejemplo:
# 2021-07-29 52122123293 Positivo
# 2021-08-01 52122123293 Negativo
def BuscarPrueba(carnet) :

    myConnection = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    cur = myConnection.cursor()
    cur.execute("""select prueba.fecha_notificacion, paciente.carnet,prueba.resultado 
from prueba prueba
inner join paciente paciente on paciente.id = prueba.paciente_id
where carnet = '%s'"""%carnet)
    msg = ''
    for fecha, carnet, resultado in cur.fetchall() :
        if resultado == None:
            resultado = 'Resultado pendiente'
        if fecha == None:
            fecha = 'Sin fecha'
        msg += str(fecha)+' '+str(carnet)+' '+str(resultado)+"\n"

    myConnection.close()
    return msg

# Creamos nuestra instancia "bot" a partir del TOKEN generado por bot father
bot = telebot.TeleBot(TOKEN)

# ------------------------------------------
# Aqui se implementan las funciones del bot

# Simple funcion de bienvenida o ayuda
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Soy un asistente para conocer el resultados de las pruebas PCR en Holguín. Para saber el resultado envíame un mensaje con tu número de carné solamente.")

# Funcion que captura el mensaje enviado y si es un carne valido lo procesa y responde
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    ci = str(message.text)
    # chequear si es un carnet de identidad valido
    if not re.match("^[0-9].{10}$", ci):
        bot.reply_to(message, "¿El número de carné es incorrecto?")
    else:
        # si es un carne valido o como minimo tiene los 11 digitos
        # entonces se llama a la funcion para buscar las pruebas que se e han hecho al paciente
        msg = BuscarPrueba(ci)
        if msg:
            bot.reply_to(message, msg)
        else:
            error = "No se han encontrado resultados para este carné de identidad."
            bot.reply_to(message, error)

# mantener "vivo" al bot
bot.polling()