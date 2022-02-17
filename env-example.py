def env(word):
    lista = {
        # "telegram-token": "[Token de telegram obtenido de @BotFather]", 
        "telegram-token": "2102316937:AAGmAMknKsYazUlQSgyY7ipTwcWhFvqe-iI", # Token Provisorio @E4K01_bot o https://t.me/E4K01_bot
        "cod-vacuna": "[Codigo-verificacion-vacuna]",
        "mongo_uri": "[ConectionString]",
        "path-chrome": '[Path del ejecutable chromedriver]',
        "nro_tramite": ""
    }
    return lista.get(word)


def get_telegram_id(nombre):
    personas = {
        "nombre": 1234567890
    }
    return personas.get(str(nombre))
