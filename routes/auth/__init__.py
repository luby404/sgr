import os
from flask import (
    Blueprint,
    request,
    url_for,
    redirect,
    session,
    render_template,
    flash
)

from models import Usuarios
from flask_login import current_user,  login_user, logout_user, login_required

auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)

@auth.get("/login")
@auth.route("/login/", methods=["GET", "POST"])
def login():
    
    
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()
        
        user:Usuarios = Usuarios.get_or_none(Usuarios.email == email)
        if user:
            if user.check_password(senha):
                flash("Usuario Logado com sucesso!")
                login_user(user)
                return redirect(url_for("dashboard.home"))
            else:
                flash("Usuario ou senha incorretos")
        else:
            flash("usuario Não existe!")
    
    return render_template("login.html")


@auth.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))