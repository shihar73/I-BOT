from .db_config import db
from .collections import user_col


col = db[user_col]

def login(user, passwd):
    print('db working')
    print(user,passwd)

    return 'seccess'