from flask import jsonify
from datetime import datetime
from helpers.db_config import db
from helpers.collections import user_col


col = db[user_col]

x = datetime.now()  

def login(user, passwd):
    login_status = {
        "status":False
    }
    user_data = col.find_one({"user_id":user})
    if user_data:
        if passwd == user_data["password"]:
            if user_data["status"]:
                del user_data["password"]
                if user_data["insta_ac"]:
                    del user_data["insta"]["passwd"]

                login_status["status"] = True
                login_status["user_data"] = user_data
                return login_status
            else:
                login_status["error_msg"] = "Your account has been disabled. Enable your account before login, please contact admin"
                login_status["error"] = "status"
        else:
                login_status["error_msg"] = "Please Check Password"
                login_status["error"] = "passwd"
    else:
        login_status["error_msg"] = "Please Check UserId"
        login_status["error"] = "user_id"

    return login_status 


def userdata(user):
    data = col.find_one({"_id": user['_id']})
    print(data["password"])
    del data["password"]
    if data["insta_ac"]:
        del data["insta"]["passwd"]
    return data


def insta_ac_add(insta, user):
    print(insta, user)
    id ={
        "_id": user['_id']
    }
    data = {"$set": {
        "insta_ac":True,
        "insta":insta
    }
    }
    col.update_one(id,data)
    return


def update_data(data, user):
    id ={
        "_id": user['_id']
    }
    data = {"$set": data
    }
    col.update_one(id,data)
    return

def user_full_data(user):
    data = col.find_one({"_id": user['_id']})
    return data

def insta_url_add(user,data):

    user['t-date'][x.strftime("%d-%m-%Y")] = len(data[1])
    id ={
        "_id": user['_id']
    }
    data = {"$set": {
        "urls":data[0],
        "todaylinks":data[1],
        "t-date":user['t-date']
    }
    }
    col.update_one(id,data)
    return


def bot_run(user):
    id ={
        "_id": user['_id']
    }
    data = {"$set": {
        "bot":True
    }
    }
    col.update_one(id,data)
    return

def bot_run_fail(user):
    id ={
        "_id": user['_id']
    }
    data = {"$set": {
        'error': f"bot running stopped on {x.strftime('%d-%m-%Y')}"
    }
    }
    col.update_one(id,data)
    return

def set_date(data):
    id ={
        "_id": data['_id']
    }
    data = {"$set": {
        "t-date": data['t-date']
    }
    }
    col.update_one(id,data)
    return


def add_start_date(user):
    id ={
        "_id": user['_id']
    }
    data = {"$set": {
        "start_date": user['start_date']
    }
    }
    col.update_one(id,data)
    return

def time_out(user):
    id ={
        "_id": user['_id']
    }
    data = {"$set": {
        "status": False,
        "bot": False
    }
    }
    col.update_one(id,data)
    return