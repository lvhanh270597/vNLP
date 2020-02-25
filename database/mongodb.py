import pymongo
from bson import ObjectId

class Connection:

    def __init__(self, host, port):
        self.client = pymongo.MongoClient(host, port)

    def auth(self, dbName, username, pwd):
        self.client[dbName].authenticate(username, pwd, mechanism='SCRAM-SHA-1', source=dbName)

    def insert(self, dbName, colName, content):
        self.client[dbName][colName].insert_one(content)
    
    def find(self, dbName, colName, query):
        data = self.client[dbName][colName].find_one(query)
        return data

    def findAll(self, dbName, colName, query):
        data = self.client[dbName][colName].find(query)
        return data

    def remove(self, dbName, colName, query):
        self.client[dbName][colName].delete_one(query)

    def update(self, dbName, colName, query, replace):
        self.client[dbName][colName].update_one(
            query, { "$set": replace }
        )

    def getAllCollections(self, dbName):
        return self.client[dbName].collection_names()