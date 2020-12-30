import os
from flask import Flask, jsonify, g
from flask_cors import CORS
import models
from flask_login import LoginManager
from blueprints.posts import post
from blueprints.users import user

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.config.update(
  SESSION_COOKIE_SECURE=True,
  SESSION_COOKIE_SAMESITE='None'
)

app.secret_key = "tyler audrey ian devin"
login_manager = LoginManager()

login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    try:
        user = models.User.get_by_id(user_id)
        return user

    except models.DoesNotExist:
        return None

CORS(post, origins=['http://localhost:3000' ,'https://the-90s-app.herokuapp.com'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000' ,'https://the-90s-app.herokuapp.com'], supports_credentials=True)

app.register_blueprint(post, url_prefix='/90s/posts/')
app.register_blueprint(user, url_prefix='/90s/users/')

@app.before_request
def before_request():
    """Connect to the db before each request"""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Connect to the db before each request"""
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hi'

if 'ON_HEROKU' in os.environ:
    print('\non heroku!')
    models.initialize()
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)