from .db_config import db
from .collections import user_col


col = db[user_col]

def login(user, passwd):
    print(user,passwd)
    login_status = {
        'status':False
    }
    user_data = [i for i in col.find({"user_id":user})]
    if user_data:
        print(user_data[0])
        if passwd == user_data[0]['password']:
            if user_data[0]['status']:
                login_status['status'] = True
                return login_status
            else:
                login_status['error_msg'] = 'Your account has been disabled. Enable your account before login, please contact admin'
                login_status['error'] = 'status'
        else:
                login_status['error_msg'] = 'Please Check Password'
                login_status['error'] = 'passwd'
    else:
        login_status['error_msg'] = 'Please Check UserId'
        login_status['error'] = 'user_id'

    return login_status 