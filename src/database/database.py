from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://dmartinez2004:ABC2357xyz@cluster0.nzc9o.mongodb.net/'
ca = certifi.where()

def db_connection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile = ca)
        db = client["sesion"]
    except ConnectionError:
        print('Error de conexion con la db')
    return db