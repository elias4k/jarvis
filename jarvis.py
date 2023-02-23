import os
import telebot

# from voicy import Voicy

bot = telebot.TeleBot(
    "2102316937:AAGmAMknKsYazUlQSgyY7ipTwcWhFvqe-iI")  # Token Provisorio @E4K01_bot o https://t.me/E4K01_bot


def message_response(message):
    try:
        #save_message(message)
        msg_to_delete = bot.send_message(message.chat.id, "A ver")
        print(str(message.chat.first_name) + ":")
        response = keyword_manager(message)
        bot.delete_message(message.chat.id, msg_to_delete.message_id)
        print(response)
    except Exception as e:
        response = e
    return response


def keyword_manager(message):
    if message.text.upper().find(":") >= 0:
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
        pass
        #return resul(data)
    elif comando == "COMMAND":
        return command(data)
    elif actions[0] == "SLUG":
        return slugger(data)
    elif comando == "NUMBERS":
        return get_numbers(message, start="", limit=4)
    elif comando == "SUM":
        return sumar(data)
    else:
        return "No entiendo tu comando"


def not_implemented():
    return "Esto todavia no esta implementado"


def sumar(numeros):
    numeros = numeros.replace(".", "").replace("\t", " ").replace("+", " ").split()
    result = 0
    for num in numeros:
        if num.isdigit():
            result = result + int(num)
    return str(result)


def talk(mensaje):
    mensaje = mensaje.replace(",", " ")
    print(mensaje)
    # Voicy.say(mensaje)
    print(not_implemented())
    return "Listo."


def slugger(text):
    char = '-'
    text = normalizeAccents(text)
    text = text.lower()
    text = text.replace('—', char)
    text = text.replace(' ', char)
    text = text.replace('(', char)
    text = text.replace(')', char)
    text = text.replace(',', char)
    text = text.replace('.', char)
    text = text.replace('°', '').replace('º', '')
    text = text.replace('--', char)
    text = text.lstrip(char)
    text = text.rstrip(char)
    return text


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


def normalizeAccents(text):
    return limpiar_acentos(text)


def command(comando):
    return not_implemented()
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
            "Cualquier consulta, comunicarse con el desarrollador"
        ]
        for row in array:
            response = response + row + "\n"
    except Exception as ex:
        response = ex
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hola " + message.chat.first_name)

@bot.message_handler(commands=['id'])
def send_id(message):
    response = "Tu ID de telegram es " + str(message.chat.id) + "1pepe"
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['userdata'])
def send_data(message):
    bot.send_message(message.chat.id, str(message).replace(",", ',\n'))


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
