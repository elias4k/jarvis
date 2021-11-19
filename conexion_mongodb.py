from os import replace
from pymongo import MongoClient

from env import *

MONGO_URI = env('mongo_uri')


def add_user(user):
    client = MongoClient(MONGO_URI)
    db = client['bots']
    collection = db['users']
    collection.insert_one(user)


def save_message(document):
    try:
        client = MongoClient(MONGO_URI)
        db = client['bots']
        collection = db['messages']
        collection.insert_one(document)
        return "Insertado"
    except Exception as ex:
        return ex

def save_pass(document):
    try:
        client = MongoClient(MONGO_URI)
        db = client['private']
        collection = db['accounts']
        collection.insert_one(document)
        return "Guardada"
    except Exception as ex:
        return ex


def update_pass(document):
    try:
        client = MongoClient(MONGO_URI)
        db = client['bots']
        collection = db['messages']
        collection.update_one({'red': document})
        return "Actualizado"
    except Exception as ex:
        return ex


def get_messages():
    try:
        client = MongoClient(MONGO_URI)
        db = client['bots']
        collection = db['messages']
        results = collection.find()
        result = ""
        for r in results:
            result = result + str(r['username']) + ": " + str(r['text']) + "\n"
        return result
    except Exception as ex:
        print(ex)
        return ex


def query_by_dni(request):
    try:
        client = MongoClient(MONGO_URI)
        db = client['padron']
        collection = db['padron_definitivo']
        results = collection.find({ "matricula" : int(request) })
        result = ""
        for r in results:
            result = result + str(r['nombre']) + ": " + str(r['apellido']) + "\n"
        return result
    except Exception as ex:
        print(ex)
        return ex


def get_pass(red):
    red = red.lower()
    try:
        print(red.upper())
        client = MongoClient(MONGO_URI)
        db = client['private']
        collection = db['accounts']
        result = collection.find_one({'red': red})
        if result:
            return result["password"]
        else:
            return "No hay coincidencias"
    except Exception as ex:
        print(ex)
        return ex


def get_users():
    try:
        client = MongoClient(MONGO_URI)
        db = client['bots']
        collection = db['messages']
        results = collection.distinct("username")
        result = ""
        for r in results:
            result = result + r + "\n"
        return result
    except Exception as ex:
        print(ex)
        return ex


class Message:
    def save(document):
        try:
            client = MongoClient(MONGO_URI)
            db = client['bots']
            collection = db['messages']
            collection.insert_one(document)
            return "Insertado"
        except Exception as ex:
            return ex


class mongo:
    def query_by_dni(request):
        try:
            client = MongoClient(MONGO_URI)
            db = client['padron']
            collection = db['padron_definitivo']
            results = collection.find({"matricula": int(request)})
            result = ""
            for r in results:
                result = result + "DNI: " + str(r['matricula']) + "\n" + "Nombre: " + str(r['nombre']) + "\n" + "Apellido: " + str(r['apellido']) + "\n" + "Clase: " + str(r['clase']) + "\n" + "Domicilio: " + str(r['domicilio']) + "\n" 
            return result
        except Exception as ex:
            print(ex)
            return ex


    def query_by(field, request):
        try:
            if field == "matricula":
                request = int(request)
            client = MongoClient(MONGO_URI)
            db = client['padron']
            collection = db['padron_definitivo']
            results = collection.find({ field : request }).limit(4)
            return results
            
        except Exception as ex:
            print(ex)
            return ex
 


class Mesa:
    def get(numero_mesa):
        numero_mesa = numero_mesa.replace(" ", "")
        try:
            client = MongoClient(MONGO_URI)
            db = client['padron']
            collection = db['mesas']
            r = collection.find_one({ "numero_mesa" : int(numero_mesa) })
            if r == None:
                return "Mesa " + str(numero_mesa) + " no participa."
            result = "Mesa: " + str(r['numero_mesa']) + "\n" \
                "Circuito: " + str(r['circuito']) + "\n" \
                "Municipio: " + str(r['nombre_municipio']) + "\n" 
            return result
        except Exception as ex:
            print(ex)
            return "Hay un problema con la mesa " + str(numero_mesa) 
