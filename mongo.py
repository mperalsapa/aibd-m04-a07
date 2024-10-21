from pymongo import MongoClient

def GetClient():
    uri = "mongodb+srv://m04.trcjf.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=M04"
    client = MongoClient(uri,
                         tls=True,
                         tlsCertificateKeyFile='./X509-cert.pem')
    return client
