from typing import Collection
from flask import *
from helpers import db_user_querys as db_user


app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form["user"] 
    passwd = request.form["password"]
    data = db_user.login(user, passwd)
    print(data)
    return render_template('home.html')

if __name__ == "__main__":
    app.run(port=6060)