# coding:utf-8
from pymongo import MongoClient

mongo = MongoClient("127.0.0.1", 27017)
db = mongo.battlefield_easy_slg


class MyModel():
    collection = None

    @classmethod
    def save(cls, _model, _dict):
        cls.collection.replace_one(_model, _dict)


class Player(MyModel):
    collection = db.player

    @classmethod
    def player_test(cls):
        player = cls.collection.find()[10]
        return player

    @classmethod
    def player_find_by_id(cls, _id):
        return cls.collection.find_one({"_id": _id})

    @classmethod
    def player_find_by_name(cls, name):
        return cls.collection.find_one({"name": name})

    @classmethod
    def player_find_and_replace_by_id(cls, _id, _dict):
        return cls.collection.replace_one({"_id": _id}, _dict)

    @classmethod
    def player_update_single_field(cls, data):
        return cls.collection.update_one({"_id": data["_id"]}, {"$set": {data["key"]: data["value"]}})
