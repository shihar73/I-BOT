from flask import jsonify
from helpers.db_config import db
from helpers.collections import user_col


col = db[user_col]

def login(user, passwd):
    login_status = {
        "status":False
    }
    user_data = [i for i in col.find({"user_id":user})]
    if user_data:
        print(user_data[0])
        if passwd == user_data[0]["password"]:
            if user_data[0]["status"]:
                del user_data[0]["password"]
                if user_data[0]["insta_ac"]:
                    del user_data[0]["insta"]["passwd"]

                login_status["status"] = True
                login_status["user_data"] = user_data[0]
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