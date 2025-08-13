import certifi
from pymongo.mongo_client import MongoClient


class NoSQLDB:
    def __init__(self):
        pass

    def client(self):
        uri = "mongodb+srv://robertsofianu:Sr25102002@cluster0.plyba0p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        return MongoClient(uri, tlsCAFile=certifi.where())

    def get_database(self, db_name):
        client = self.client()
        return client[db_name]

    def add_collection_to_database(self, db_name, collection_name):
        db = self.get_database(db_name)
        db.create_collection(collection_name)

    def add_json_to_collection(self, db_name, collection_name, json_data):
        db = self.get_database(db_name)
        collection = db[collection_name]
        collection.insert_one(json_data)

if __name__ == "__main__":
    db = NoSQLDB()
    db.add_json_to_collection("invoices", "invoices", {"item": "item1", "price": 100})