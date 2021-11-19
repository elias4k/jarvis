def env(word):
    lista = {
        "telegram-token": "[Token de telegram obtenido de @BotFather]", 
        "cod-vacuna": "[Codigo-verificacion-vacuna]",
        "mongo_uri": "[ ConectionString]",
        "path-chrome": '[Path del ejecutable chromedriver]',
    }
    return lista.get(word)


def get_telegram_id(nombre):
    personas = {
        "nombre": 1234567890
    }
    return personas.get(str(nombre))
