import pyttsx3

class Voicy():

    def say(mensaje):
        engine = pyttsx3.init()
        engine.setProperty('voice', '''HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0''')
        engine.setProperty('rate', 150)
        engine.say(mensaje)
        engine.runAndWait()

    def get_props():
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            print(voice)


def main():
    #Voicy.say("Hola, bienvenido")
    Voicy.get_props()


if __name__ == '__main__':
    main()