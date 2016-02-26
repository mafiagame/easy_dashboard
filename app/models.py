# coding:utf-8
import os
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

    @classmethod
    def player_compensate(cls, data):
        updater = {}
        for key in data:
            if key == "diamond":
                updater["resource.diamond"] = int(data[key])
            elif key in ["units", "items"]:
                for _id in data[key]:
                    updater["%s.%s" % (key, _id)] = int(data[key][_id])
        if updater:
            Player.collection.update_many({}, {
                "$inc": updater
            })


if __name__ == "__main__":
    import imp
    import sys
    fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'easy_slg/model/mail.py')
    _dir1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'easy_slg/')
    _dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'easy_slg/model')
    _dir3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'easy_slg/utils')
    sys.path.append(_dir1)
    sys.path.append(_dir2)
    sys.path.append(_dir3)

    foo = imp.load_source('module.name', fp)
    foo.MyClass()
    foo.Mail.send_system_all_mail('test_sys_title_mail', {'text': 'test_sys_mail_content'})