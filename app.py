from logging import fatal
from flask import *
from functools import wraps
from helpers import db_user_querys as db_user
from insta.bot import Bot
from datetime import timedelta


app = Flask(__name__)
app.secret_key = b'|\xe5YHYU\xadY\x9c\xf2%\xc1\xe0\xb5\xf4W'



@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=300)


def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')

  return wrap


@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for("home"))

    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    
    user = request.form["user"] 
    passwd = request.form["password"]
    data = db_user.login(user, passwd)
    if data['status']:
        session['logged_in'] = True
        session['user'] = data['user_data']
        print(session['user'])
        return redirect(url_for("home"))
        
    else:
        flash(data['error_msg'],data['error'])
        return redirect(url_for("index"))


@app.route('/home')
@login_required
def home():
    data = db_user.userdata(session['user'])
    return render_template('home.html', data = data)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route('/instalogin', methods=['POST'])
@login_required
def insatlogin():

    insta_id = request.form["instaid"] 
    passwd = request.form["password"]
    insta ={
        "insta_id" : insta_id, 
        "passwd" : passwd
    }
    bot = Bot(insta_id,passwd)
    data = bot.login()
    if data:
        print(data)
        bot.exit()
        return jsonify(status = False, msg = data)
    else:
        bot.exit()
        session['user']["insat_ac"] = True
        session['user']["insta"] = {
        "insta_id" : insta_id
    }
        user = session['user']
        db_user.insta_ac_add(insta,user)
        return jsonify(status = True, msg = f"Your {insta_id} insta account has been added successfully")



@app.route('/data', methods=['POST'])
@login_required
def data():
    data = {}
    data["tags"] = request.form["tags"].replace(" ", "").split(",")
    data["comments"] = request.form["comments"].split(",")
    print(len(data["tags"]), len(data["comments"]))
    if len(data["tags"]) >= 5 and len(data["comments"]) >= 5:
        print('add in database')
        db_user.update_data(data, session['user'])
        return jsonify(status = True, msg = f"Your data has been added successfully")
    else:
        return jsonify(status = False, msg = f"Please Keep Minimum")



if __name__ == "__main__":
    app.run()