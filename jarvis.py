# pip install pip 
# pip install pyTelegramBotAPI selenium pymongo
import os
import telebot
from selenium import webdriver
from conexion_mongodb import *
from env import *
import requests
from time import sleep, time
from selenium.webdriver.support.ui import Select
from datetime import datetime
from env import *
#from voicy import Voicy

bot = telebot.TeleBot("2102316937:AAGmAMknKsYazUlQSgyY7ipTwcWhFvqe-iI") # Token Provisorio @E4K01_bot o https://t.me/E4K01_bot


def message_response(message):
    try:
        save_message(message)
        msg_to_delete = bot.send_message(message.chat.id, "A ver")
        print(str(message.chat.first_name) + ":")
        response = keyword_manager(message)
        bot.delete_message(message.chat.id, msg_to_delete.message_id)
        print(response)
    except Exception as e:
        response = e
    return response


def keyword_manager(message):
    if message.text.upper().find("Tu ID de telegram es ".upper()) >= 0:
        bot.send_message(message.chat.id, str(message.forward_from).replace(",", ',\n'))
        return add_telegram_user(message)

    elif message.text.upper().find("NUMBERS") >= 0:
        if message.text.upper().find("NUMBERS=") >= 0:
            start = message.text.upper().find("NUMBERS=") + len("NUMBERS=")
            msg_temp = message.text.upper()[start:]  
            if msg_temp.find(" ") >= 0:
                msg_temp = msg_temp[:msg_temp.find(" ")]
            start_word = msg_temp
        else:
            start_word = ":"
        response = get_numbers(message, start=start_word, limit=4)
        return response

    elif message.text.upper().find(":") >= 0:
        response = command_manager(message.text.upper(), message)
        return response
    else:
        response = "No te entiendo"
        return response


def command_manager(mensaje, message):
    array = mensaje.split(":", 1)

    actions = array[0].split(".")
    comando = actions[0]
    data = array[1]
    if comando == "RESUL":
        return resul(data)
    elif comando == "COMMAND":
        return command(data)
    elif comando == "MESA":
        return get_mesa(data, message)
    elif comando == "NUMBERS":
        return get_numbers(message, start="", limit=4)
    elif comando == "TALK":
        return talk(data)
    elif comando == "SUM":
        return sumar(data)
    elif comando == "INFOVACUNA":
        print("Info Vacuna: " + data + "\n\n")
        return infovacuna(data, message)
    elif comando == "Q":
        if len(actions) >= 2:
            if actions[1] == "A":
                return query(data, message, field="apellido")
            elif actions[1] == "N":
                return query(data, message, field="nombre")
        else:
            return query(data, message)
    elif comando == "APAGAR":
        print("Apagar equipo: \n")
        return command("shutdown -s")
    else:
        return "No entiendo tu comando"


def not_implemented():
    response = "Esto todavia no esta implementado"
    print(response)
    return response


def sumar(numeros):
    numeros = numeros.replace(".", "")
    numeros = numeros.replace("\t", " ")
    numeros = numeros.replace("+", " ")
    numeros = numeros.split()
    result = 0
    for num in numeros:
        if num.isdigit():
            result = result + int(num)
    return str(result)


def open_link(data):
    try:
        data = data.replace(" ", "")
        driver = browser()
        driver.maximize_window()
        driver.get(data)
        response = driver.title
    except Exception as ex:
        print(ex)
        response = ex
    return response


def talk(mensaje):
    mensaje = mensaje.replace(",", " ")
    print(mensaje)
    #Voicy.say(mensaje)
    print(not_implemented())
    return "Listo."

    
def get_mesa(msg, message):
    msg = msg.replace("\n", ",").replace(" ", ",").replace(" ", "")
    array = msg.split(",")
    mensajes = []
    #Voicy.say(mensaje)
    for mesa in array:        
        if mesa.isdigit():
            mensajes.append(bot.send_message(message.chat.id, Mesa.get(mesa), disable_notification=True).message_id)
    sleep(10)
    for m in mensajes:
        bot.delete_message(message.chat.id, m)
    return "Listo."


def consulta_padron(dni):
    try:
        tiempo_inicio = time()
        p = query(dni)
        if p == "404":
            return "Persona no encontrada. Intentelo nuevamente"
        datos = [
            p.apellido + ", " + p.nombre,
            "DNI: " + p.matricula + " " + p.tipo_ejemplar,
            "Municipio: " + p.ley_mun,
            "Establecimiento: " + p.establecimiento,
            "Direccion: " + p.lugar,
            "Nro de Mesa: " + p.nro_mesa,
            "Nro de Orden: " + p.orden_mesa,
        ]
        response = ""
        for dato in datos:
            response = response + str(dato) + "\n"
        tiempo = time() - tiempo_inicio
        response = response + "\nTiempo de ejecución: " + str(round(tiempo, 3)) + " segundos"
        return response
    except:
        return "Se ha producido un error"


def resul(data):
    data = data.split("-")
    if len(data) > 1:
        tramite = data[1]
    else:
        tramite = env("nro_tramite")
    persona = {
        'dni': str(data[0]),
        'nro_tramite': str(tramite)
    }
    driver = browser()
    driver.get('https://permisos.corrientes.gob.ar/testeocovid')
    driver.find_element_by_xpath('//*[@id="dni"]').send_keys(persona.get('dni'))
    driver.find_element_by_xpath('//*[@id="nro_tramite"]').send_keys(persona.get('nro_tramite'))
    driver.find_element_by_xpath('//*[@id="app"]/main/div/div/div/div/div[2]/form/input[2]').click()
    contenido = driver.find_element_by_xpath('/html/body/div/main/div/div/div/div').text
    contenido = contenido.replace("VOLVER", "")
    driver.quit()
    return contenido


def infovacuna(mensaje, message):
    print(mensaje)
    mensaje = mensaje.replace(".", "")
    mensaje = mensaje.replace(" ", "")
    array_dnis = mensaje.split(',')
    cod = env("cod-vacuna")
    try:
        driver = browser()
        for dni in array_dnis:
            dni = str(dni).upper()
            ss = dni.upper().find("M")
            if dni.upper().find("F") >= 0:
                sexo = "Femenino"
                dni = str(dni).replace("F", "").replace("f", "")

            elif dni.upper().find("M") >= 0:
                sexo = "Masculino"
                dni = str(dni).replace("M", "").replace("m", "")
            else:
                result = "Debe indicar el sexo con F o M"
                print(result)
                driver.quit()
                return result

            if dni.isdigit():
                try:
                    driver.get("https://vacunate.corrientes.gob.ar/vacunate/verificar")
                    driver.find_element_by_xpath('//*[@id="dni"]').send_keys(dni)
                    select_sexo = Select(driver.find_element_by_xpath('//*[@id="sexo"]'))
                    select_sexo.select_by_visible_text(sexo)
                    driver.execute_script("document.getElementById('codigo').setAttribute('type', 'password')")
                    driver.find_element_by_xpath('//*[@id="codigo"]').send_keys(cod)
                    driver.find_element_by_xpath('//*[@id="app"]/main/div/div/div/div/div[2]/form/input[2]').click()
                    sleep(1)
                    estado = driver.find_element_by_xpath(
                        '//*[@id="app"]/main/div/div/div/div').text
                    estado = estado.replace("Descargar comprobante de Inscripción", "")
                    estado = estado.replace("Descargar turno de Primera Dosis", "")
                    estado = estado.replace("Datos obtenidos del RENAPER", "")
                    estado = estado.replace("Editar Información", "")
                    estado = estado.replace("Quiero cancelar mi inscripción", "")
                    estado = estado.replace("Volver", "")
                    estado = estado.replace("Si existe algún error u omisión en los datos llame al 0800-444-0978.", "")
                except:
                    estado = " no encontrado"
                bot.reply_to(message, dni + ": " + estado)
            # bot.reply_to(message, dni + ":\n" + estado_inscripcion + "\n" + cod_inscripcion)
            else:
                bot.reply_to(message, dni + ": Esto ni siquiera es un número")
        print("Cantidad de DNIs: " + str(len(array_dnis)))
    except Exception as ex:
        return ex
    try:
        sleep(5)
        driver.quit()
    except Exception as ex:
        print(ex)
    respuesta = "Listo."
    return respuesta


def get_fecha_nac_vacunate(dni):
    cod = env("cod-vacuna")
    respuesta = ""
    try:
        driver = browser()
        dni = str(dni).upper()
        if dni.upper().find("F") >= 0:
            sexo = "Femenino"
            dni = str(dni).replace("F", "").replace("f", "")

        elif dni.upper().find("M") >= 0:
            sexo = "Masculino"
            dni = str(dni).replace("M", "").replace("m", "")
        else:
            result = "Debe indicar el sexo con F o M"
            print(result)
            return result

        if dni.isdigit():
            try:
                driver.get("https://vacunate.corrientes.gob.ar/vacunate/verificar")
                driver.find_element_by_xpath('//*[@id="dni"]').send_keys(dni)
                select_sexo = Select(driver.find_element_by_xpath('//*[@id="sexo"]'))
                select_sexo.select_by_visible_text(sexo)
                driver.execute_script("document.getElementById('codigo').setAttribute('type', 'password')")
                driver.find_element_by_xpath('//*[@id="codigo"]').send_keys(cod)
                driver.find_element_by_xpath('//*[@id="app"]/main/div/div/div/div/div[2]/form/input[2]').click()
                fecha_nac = driver.find_element_by_xpath(
                    '//*[@id="app"]/main/div[1]/div/div/div/div[2]/ul/li[6]').text
                fecha_nac = fecha_nac.split("(")[0]
                fecha_nac = fecha_nac.replace("Fecha de Nacimiento:", "")
                fecha_nac = fecha_nac.replace(" ", "")
                if len(fecha_nac) > 0:
                    respuesta = fecha_nac
                else:
                    respuesta = ""
            except Exception as ex:
                respuesta = ""
        else:
            respuesta = ""
        driver.quit()
    except Exception as ex:
        return ""
    return respuesta


def command(comando):
    try:
        if comando.upper() == "APAGAR":
            comando = "shutdown -s"
        if comando.upper() == "APAGARF":
            comando = "shutdown -s -t 10"
        if comando.upper() == "REINICIAR":
            comando = "shutdown -r"
        response = os.system(comando)
    except Exception as e:
        response = e
    return response


def get_numbers(message, start="", limit=4, divided=False, orded=True):
    start = start.lower()
    mensaje = message.text.upper()
    mensaje = mensaje.replace(",", " ").replace(".", " ")
    mensaje = mensaje.replace("\n", " ")
    words = mensaje.split()
    numbers_array = []
    number_string: str = ""
    for word in words:
        if word.isdigit() and len(word) <= limit:
            numbers_array.append(word)
    numbers_array = list(set(numbers_array))  # Delete duplicates // Convert a Set Object to list
    if orded:
        numbers_array = ordenarStrList(numbers_array)
    """
    # No optimizado para esta version
    if divided:
        if (len(numbers_array) % 2) > 0:
            mitad = (len(numbers_array) - 1) / 2
        else:
            mitad = len(numbers_array) / 2
        print(str(int(mitad)))
        numbers_array0 = numbers_array[0:int(mitad)]
        numbers_array1 = numbers_array[int(mitad):len(numbers_array)]
        dnistring0 = dnistring1 = ":"
        for dni in numbers_array0:
            dnistring0 = dnistring0 + "," + dni
        for dni in numbers_array1:
            dnistring1 = dnistring1 + "," + dni
            
        dnistring0 = dnistring0.replace(":", "")
        dnistring1 = dnistring1.replace(":,", "")
        bot.send_message(message.chat.id, start + dnistring0)
        bot.send_message(message.chat.id, start + dnistring1)'
    """
    for number in numbers_array:
        number_string = number_string + "," + number
    number_string = number_string[1:]
    # number_string = number_string.replace(",", "")
    # number_string = number_string.replace(":", "")
    if len(numbers_array) < 1:
        return "No encontré numeros en tu mensaje capo"
    else:
        bot.send_message(message.chat.id, str(len(numbers_array)) + " numeros encontrados.")
    return start + number_string
    # return number_string


def ordenarStrList(array_str):
    array_number = []
    new_array_str = []
    for dni_str in array_str:
        array_number.append(int(dni_str))
    array_number.sort()
    for dni_number in array_number:
        new_array_str.append(str(dni_number))
    return new_array_str


def limpiar_acentos(text):
    text = text.replace("á", "a")
    text = text.replace("é", "e")
    text = text.replace("í", "i")
    text = text.replace("ó", "o")
    text = text.replace("ú", "u")
    text = text.replace("Á", "A")
    text = text.replace("É", "E")
    text = text.replace("Í", "I")
    text = text.replace("Ó", "O")
    text = text.replace("Ú", "U")
    return text


def browser():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        web_driver = webdriver.Chrome('chromedriver.exe', options=options)
    except:
        try:
            print("Error al abrir Chrome")
            web_driver = webdriver.Edge()
        except:
            print("Error al abrir Edge")
            print("Abriendo con Firefox")
            web_driver = webdriver.Firefox()
    return web_driver


def query(data, message, field="matricula"):
    try:
        data = limpiar_acentos(data).upper().strip()
        data = data.replace("APELLIDO", "").replace("NOMBRE", "").replace("MATRICULA", "")
        if message.chat.id == get_telegram_id("elias"):
            if data.isdigit() and False:
                result = mongo.query_by("matricula", data)
                bot.send_message(message.chat.id, result)
            else:
                results = mongo.query_by(field, data.strip())
                for r in results:
                    nac = get_fecha_nac_vacunate(r['genero'] + str(r['matricula']))
                    if len(nac) > 0:
                        nac = "Fecha Nac: " + nac
                    else:
                        nac = "Clase: " + str(r['clase'])
                    result = "DNI: " + str(r['matricula']) + "\n" + "Nombre: " + str(
                        r['nombre']) + "\n" + "Apellido: " + str(r['apellido']) + "\n" + "Género: " + str(
                        r['genero']) + "\n" + "Domicilio: " + str(r['domicilio']) + "\n" + "Municipio: " + str(
                        r['ley_mun']) + "\n" + nac
                    bot.send_message(message.chat.id, result)
            return "Listo"
        else:
            return "Acceso no autorizado."
    except Exception as ex:
        bot.send_message(message.chat.id, field + data)
        return ex


def save_p(text):
    text.replace(",", "\n")
    data = text.split("\n")
    document = {
        "nombre": data[0],
        "email": data[1],
        "p": data[2],
        "username": data[3],
    }
    result = save_pass(document)
    return result


@bot.message_handler(commands=['help', 'ayuda'])
def comandos_helper(message):
    response = ""
    try:
        array = [
            "Podes elegir entre las siguientes opciones:",
            "",
            "",
            "/comandos: Para ver este mensaje.",
            "",
            "/id: para obtener tu ID de Telegram.",
            "",
            "resul: Para obtener el listado de los testeos realizados a esa persona. se debe enviar DNI y Nro de tramite separados por un guión. Ej:",
            "resul:35123456-00356813548",
            "",
            "Infovacuna: Obtiene informacion del turno de vacunacion. Se pueden consultar varios a la vez indicando el sexo con F o M junto a cada DNI. Ej:",
            "Infovacuna:m40.111666, f17739478, 2.567.893M, 10333f890",
            "",
            "Cualquier consulta, comunicarse con el desarrollador"
        ]

        for row in array:
            response = response + row + "\n"
    except Exception as ex:
        response = ex
    #bot.send_message(message.chat.id, get_saludo() + " " + message.chat.first_name)
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hola " + message.chat.first_name)
    bot.send_message(get_telegram_id("elias"), message.chat.first_name + " ha iniciado el bot.")
    bot.send_message(get_telegram_id("elias"), str(message.chat.id))


@bot.message_handler(commands=['id'])
def send_id(message):
    response = "Tu ID de telegram es " + str(message.chat.id)
    bot.send_message(message.chat.id, response)
    bot.send_message(get_telegram_id("elias"), message.chat.first_name + " ha solicitado su ID de Telegram.")
    bot.send_message(get_telegram_id("elias"), str(message.chat.id))


@bot.message_handler(commands=['mensajes'])
def get_mensajes(message):
    bot.send_message(message.chat.id, get_messages())


@bot.message_handler(commands=['usuarios'])
def get_usuarios(message):
    bot.send_message(message.chat.id, get_users())


@bot.message_handler(commands=['userdata'])
def send_data(message):
    bot.send_message(message.chat.id, str(message).replace(",", ',\n'))


@bot.message_handler(commands=['reiniciar'])
def send_data(message):
    command("REINICIAR")
    bot.send_message(message.chat.id, "Reiniciando...")


@bot.message_handler(commands=['apagar'])
def send_data(message):
    command("APAGAR")
    bot.delete_message(message.chat.id, bot.send_message(message.chat.id, "Apagando").message_id)


@bot.message_handler(commands=['cancelar'])
def send_data(message):
    command("shutdown -a")
    bot.send_message(message.chat.id, "Cancelando apagado..")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def respuesta_text(message):
    try:
        print(message.text)
        response = message_response(message)
        if response == "null" or response is None:
            response = ""
        if response != "":
            bot.send_message(message.chat.id, response, disable_notification=True)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(func=lambda message: True, content_types=['voice'])
def respuesta_audio(message):
    try:
        bot.reply_to(message, "Ahora no puedo escuchar audio bro, mejor escribí")
    except Exception as e:
        bot.reply_to(message, e)


bot.polling()
