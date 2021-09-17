import pymongo
import bcrypt


class DictionaryDB:
    mongo_uri = "mongodb://localhost:27017/"
    database = None
    nested_data = None
    users = None
    flat_data = None

    @staticmethod
    def create_db():
        mongo_client = pymongo.MongoClient(DictionaryDB.mongo_uri)
        DictionaryDB.database = mongo_client["nested_app_db"]
        DictionaryDB.flat_data = DictionaryDB.database["flat_data"]
        DictionaryDB.nested_data = DictionaryDB.database["nested_data"]
        DictionaryDB.users = DictionaryDB.database["credentials"]
        DictionaryDB.add_test_user("example_user", "example_password")

    @staticmethod
    def insert_dictionary_data(username, dict_type, data):
        input_data = {"username": username, "data": data}

        if DictionaryDB.nested_data.find_one({"username": username}):
            DictionaryDB.nested_data.delete_many({"username": username})
        if dict_type == "raw":
            if DictionaryDB.flat_data.find_one({"username": username}):
                DictionaryDB.flat_data.delete_many({"username": username})
            DictionaryDB.flat_data.insert(input_data)
        else:
            DictionaryDB.nested_data.insert(input_data)

    @staticmethod
    def get_dictionary_data(username, data_type):
        if data_type == "raw" and DictionaryDB.flat_data.find_one({"username": username}):
            return DictionaryDB.flat_data.find_one({"username": username})["data"]
        elif data_type == "nested" and DictionaryDB.nested_data.find_one({"username": username}):
            return DictionaryDB.nested_data.find_one({"username": username})["data"]

    @staticmethod
    def get_hashed_pw(username):
        return DictionaryDB.users.find_one({"username": username})

    @staticmethod
    def is_user(username):
        users = DictionaryDB.users.distinct("username")
        if username not in users:
            return False
        return True

    @staticmethod
    def add_test_user(username, password):
        salt = bcrypt.gensalt(rounds=10)
        password = password
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        if DictionaryDB.nested_data.find_one({"username": username}):
            DictionaryDB.users.delete_many({"username": username})
        DictionaryDB.users.insert({"username": username, "password": hashed})
