from flask import Flask, jsonify, g
from flask_cors import CORS
import models
from flask_login import LoginManager
from blueprints.posts import post
from blueprints.users import user

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.secret_key = "tyler audrey ian devin"
login_manager = LoginManager()

login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    try:
        print("loading the following user")
        user = models.User.get_by_id(user_id)
        return user

    except models.DoesNotExist:
        return None

CORS(post, origins=['http://localhost:3000'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(post, url_prefix='/90s/posts/')
app.register_blueprint(user, url_prefix='/90s/users/')

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hi'
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)