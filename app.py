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
    print(data)
    if data['status']:
        session['logged_in'] = True
        session['user'] = data['user_data']
        return redirect(url_for("home"))
        
    else:
        flash(data['error_msg'],data['error'])
        return redirect(url_for("index"))


@app.route('/home')
@login_required
def home():
    print(session)
    data = session['user']
    # data['bot'] = True
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
    bot = Bot(insta_id,passwd)
    data = bot.login()
    data = False
    if data:
        print(data)
        bot.exit()
        return jsonify(status = False, msg = data)
    else:
        bot.exit()
        session["insat_ac"] = True
        return jsonify(status = True, msg = f"Your {insta_id} insta account has been added successfully")



if __name__ == "__main__":
    app.run()