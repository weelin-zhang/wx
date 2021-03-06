from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.config.from_object('config')
#print app.config['SECRET_KEY']
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'admin.login'
login_manager.login_message = ''
login_manager.init_app(app)
bootstrap = Bootstrap(app)
from app import views
