import os
from flask import *

from models import Usuario
from flask_login import login_user, logout_user, login_required

auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)


@auth.route("/login/", methods=["GET", "POST"])
@auth.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()
        
        user:Usuario = Usuario.get_or_none(Usuario.email == email)
        
        print(user)
        if user:
            if user.check_password(senha):
                login_user(user)
                next_page = request.args.get("next")
                if user.user_type in [user.roles.gestor]:
                    return redirect(next_page or url_for("admin.index"))
                else:
                    return redirect(url_for("dashboard.index", name="home"))
            else:
               flash("Usuario ou senha Incorretos!") 
        else:
            flash("Usuario ou senha Incorretos!")
        
    
    return render_template("auth.login.html")




@auth.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

