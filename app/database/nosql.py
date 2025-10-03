# Importacion de los frameworks
from pymongo import MongoClient
import certifi, os

# Acceso de la base de datos
mongo_uri = os.getenv('MONGO_URI', 'mongo atlas')
mongo_db = os.getenv('MONGO_DB', 'sesion')
ca = certifi.where()
client = MongoClient(mongo_uri, tlsCAFile = ca)

# Conexion de la base de datos
def db_connection():
    try:
        # Selección de la base de datos
        db = client[mongo_db]
    except ConnectionError:
        print('Error de conexion con la db')
    return db

def count_collection():
    # Selección de la base de datos
    db = client[mongo_db]
    # Obtener todas las colecciones
    names = db.list_collection_names()
    # Contar documentos en cada colección
    print(f"'Numero de colecciones': {len(names)}")
    for name in names:
        docs = db[name].count_documents({})
        print(f"Colección '{name}': {docs} documentos")

def create_database(db_name):
    # Crear base de datos
    db = client[db_name]
    # Crear las colecciones
    collections = {'customers','products','stores','orders'}
    for col in collections:
        db.create_collection(col)