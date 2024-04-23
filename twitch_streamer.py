import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
import pyttsx3
import os
import threading




def Silv_CORE(msg_for_silv):
    # Esperar hasta que cargue la caja de texto
    caja_de_chat = WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.NAME, "content"))
    )

    caja_de_chat.send_keys(msg_for_silv)  # Mensaje aquí
    caja_de_chat.send_keys(Keys.RETURN)  # Presiona el ENTER

    # En caso la coneccion sea lenta aumentar tiempo a ejecutarse
    time.sleep(0)

    def generador_Respuesta():
        global Silv_respuesta
        global lista_2
        while True:
            # Esperar a que al menos uno de los elementos con data-testid="final-bot-response" esté presente
            cuadros_respuesta = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="final-bot-response"] > p'))
            )

            # Imprimir solo la última respuesta
            lista_1 = [cuadro.text for cuadro in cuadros_respuesta[
                                                 -3:]]  # Esto solo trae los 7 ultimos para evitar que se le llena la memoria con la lista
            lista_sin_repetidos = [x for x in lista_1 if
                                   x not in lista_2]  # borra los elementos que contiene la lista anterior a la nueva
            ultima_respuesta = '\n'.join(lista_sin_repetidos)
            # Si la lista esta vacia significa que saco el mismo valor dos veces asi que enviar a repetir la funcion hasta que encuentre un valor diferente
            if lista_sin_repetidos != []:
                Silv_respuesta = ultima_respuesta

                print(f"Silv: {Silv_respuesta}")
                lista_2 = [cuadro.text for cuadro in cuadros_respuesta[-7:]]
                voice_silv(Silv_respuesta) #Crea el archivo de voz sin filtro de Txt to Speach
                try:
                    while True:
                        ruta_autor = "autorisation"
                        autor = open(ruta_autor, 'r', encoding='utf-8').read()

                        if autor == "yes":

                            def ejecutar_realtek():
                                subprocess.run(["python", "play_realtek.py"], shell=True)

                            threading.Thread(target=ejecutar_realtek).start()
                            break  # IMPORTANTE este break evita que el loop destruya la pc CUIDADO!!!
                    break
                except:
                    print("error modulo voz")

            else:
                pass


    generador_Respuesta()

#########################################
#Es para asegurar que la autorizacion sea positiva a la hora de iniciar por primera vez
ruta_autor = "autorisation"
ruta_msg_silv = "mensaje_silv"
with open(ruta_autor, 'w') as archivo:
    archivo.write("yes")
with open(ruta_msg_silv, 'w') as archivo:
    archivo.write("k9Tp2")
########################################
def voice_silv(reprodu):
    # Inicializar el motor de texto a voz
    engine = pyttsx3.init()

    # Obtener todas las voces disponibles
    voices = engine.getProperty('voices')

    # Establecer la voz de mujer
    for voice in voices:
        # Encuentra una voz de mujer (cambiar "female" por "male" para voz masculina)
        if "female" in voice.name:
            engine.setProperty('voice', voice.id)
            break

    # Establecer el texto que deseamos convertir en voz
    texto_a_voz = reprodu

    # Convertir el texto en voz
    engine.save_to_file(texto_a_voz, 'repro.mp3')
    engine.runAndWait()

def revision_de_msg_text():
    with open(ruta_msg_silv, 'r', encoding="utf-8") as archivo:
        global text_input
        text_input = archivo.read()

def chat_Twitch():
    try:
        #Pide info al Node.js
        #response = requests.get('http://127.0.0.1:8080/obtener_ultimo_mensaje')
        response = requests.get('http://127.0.0.1:3000/obtener_ultimo_mensaje')
        response.encoding = "utf-8" #Codifica a utf8 (evita errores en las tildes)
        global ultimo_mensaje
        ultimo_mensaje = response.text
    except:
        pass

Silv_respuesta = None
lista_2 = [] #esto le da valor a lista 2 para que pueda dar la primera vuelta sin errores
###########################
chat_Twitch()
print(ultimo_mensaje)
valor_anterior = ultimo_mensaje
#############################

##################################
"""AQUI ABAJO VA LA URL DEL CHATBOT A SCRAPEAR"""
url_pagina = "" #AQUI EL URL
chrome_options = Options()
chrome_options.add_argument("--headless") #puedes quitarle una letra si deaseas que abra la instansia del driver para revisar manualmente

# Crear una instancia del navegador (abre el chromedriver de la carpeta)
driver = webdriver.Chrome(options=chrome_options)
#################################
try:
    driver.get(url_pagina)
    time.sleep(5)
    while True:  # Verificar si se envió un nuevo mensaje
        chat_Twitch()
        time.sleep(0)
        #revision_de_msg_text() #obtiene el valor del text_input
        if "!ign" in ultimo_mensaje:
            """
            Si en el mensaje del chat enncuentra que se uso !ign lo ignora funcion añadida para poder responder dudas sin llamar a la ia
            """
            pass

        elif ultimo_mensaje != valor_anterior: # recibe el mensaje de twitch si es diferente
            print(f"chat:{ultimo_mensaje}")

            Silv_CORE(ultimo_mensaje)
            valor_anterior = ultimo_mensaje #Guarda el ultimo mensaje

finally:
    # Cerrar el navegador al salir del bucle
    driver.quit()

