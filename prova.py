from pymongo import MongoClient

uri = "mongodb+srv://m04.trcjf.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=M04"
cliente = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='./X509-cert.pem')

iabd_db = cliente.iabd


# Recuperamos las colecciones
print(iabd_db.list_collection_names())
people_coll = iabd_db.people


# Recuperamos una persona
persona = people_coll.find_one()
print(people_coll.count_documents({}))
print(persona)

# Conteo de peliculas
# mflix = cliente.sample_mflix
# movies = mflix.movies
# doc_count = movies. count_documents({})
# print("{} movies in movie collection".format(doc_count))

# Listar peliculas de salma hayek
# cursor = movies.find({"cast": "Salma Hayek"})
# for pelicula in cursor:
#     print(pelicula["title"])

# Insertar un registro
# paco = {"nombre": "Paco", "edad": 22, "profesion": "estudiante"}
# people_coll.insert_one(paco)
# print(people_coll.count_documents({}))

# Modificar un registro
people_coll.update_one({"nombre": "Paco"}, {"$set": {"nombre": "Paquito"}})
persones = people_coll.find({})
for persona in persones:
    print("Persona encontrada: {}".format(persona["nombre"]))