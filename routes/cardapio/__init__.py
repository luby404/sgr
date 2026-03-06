import os
from flask import (
    Blueprint,
    request,
    url_for,
    redirect,
    session,
    render_template
)

cardapio = Blueprint(
    "cardapio",
    __name__,
    url_prefix="/cardapio",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)


@cardapio.get("/")
def index():
    
    class dados:
        intens_carrinho = 0
        produtos   = []
        categorias = []
    
    return render_template("cardapio.index.html", dados=dados)


@cardapio.route("/produto")
def produto():
    return render_template("cardapio.produto.html")


@cardapio.route("/carrinho", methods=["POST", "GET", "DELETE"])
def carrinho():
    
    if request.method == "POST":
        session["carrrinho"] = {}
        
        return redirect(url_for("cardapio.index"))
    
    return render_template("cardapio.carrinho.html")

