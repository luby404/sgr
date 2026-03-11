from flask import Flask
from flask_login import LoginManager
from models import Usuario


login = LoginManager()
login.login_view = "auth.login"

@login.user_loader
def load_user_auth(id):
    return Usuario.get_or_none(Usuario.id == id)

def init_auth(app: Flask):
    login.init_app(app)