from flask import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form["user"]
    passwd = request.form["password"]
    print(user,passwd)

    return render_template('home.html')

if __name__ == "__main__":
    app.run()