import os
from flask import (
    Blueprint,
    request,
    url_for,
    redirect,
    session,
    render_template
)

from .views import pages

produtos = Blueprint(
    "produtos",
    __name__,
    url_prefix="/produtos",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)


@produtos.get("/<name>")
def index(name=None):
    class Dados:
        ...
    if name in pages:
        return render_template(pages[name], dados=Dados)
    
    return render_template("404.html")

@produtos.post("/action/new")
def new():
    
    empresa = 0
    
    nome      = request.form.get("nome", "")
    price     = request.form.get("price", 0)
    descricao = request.form.get("descricao", "")
    categoria = request.form.get("categoria", "")
    
    file = request.files.get("capa", None)
    if file:
        ...
    
    print("Novo Produto Cadastrodado com sucesso")
    
    return redirect(url_for("dashboard.index", name='produto'))
    
    