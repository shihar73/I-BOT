from typing import Collection
from flask import *
from helpers import db_user_querys as db_user


app = Flask(__name__)
app.secret_key = "dont tell"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form["user"] 
    passwd = request.form["password"]
    data = db_user.login(user, passwd)
    print(data)
    if data['status']:
        return render_template('home.html')
    else:
        flash(data['error_msg'],data['error'])
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(port=6060)