import os, uuid
from flask import *

from .views import pages


from models import Empresa, Produto, Categoria, Usuario

from utils import BASE_DIR

produtos = Blueprint(
    "produtos",
    __name__,
    url_prefix="/produtos",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)

from flask_login import login_required, current_user

current_user:Usuario

@produtos.route("/<name>", methods=["GET", "POST", "PUT", "DELETE"])
def index(name=None):
    
    
    class Dados:
        categorias = (cate for cate in Categoria.select().where(
            (Categoria.is_ative == True) & 
            (Categoria.empresa == current_user.empresa)
        ))
        produtos = (
            produto
            for produto in Produto.select().where(
                (Produto.is_ative == True) & 
                (Produto.empresa == current_user.empresa)
            )
        )
        
        empresa_id = str(current_user.empresa.id)
        
        
    if name in pages:
        return render_template(pages[name], dados=Dados)
    
    return render_template("404.html")

@produtos.post("/action/new")
def new():
    
    empresa = Empresa.get_or_none(Empresa.id == current_user.empresa)
    
    nome      = request.form.get("nome", "")
    price     = request.form.get("price", 0)
    descricao = request.form.get("descricao", "")
    categoria = Categoria.get_or_none(Categoria.id == request.form.get("categoria", ""))
    
    file = request.files.get("capa", None)
    filename = ""
    if file and empresa:
        empresa_id = str(empresa.id)
        filename = f"{uuid.uuid4()}_{file.filename}"
        path = os.path.join(BASE_DIR, f"empresa_{empresa_id}")
        if not os.path.exists(path): os.mkdir(path)
        
        file.save(os.path.join(path, filename))
    
    if empresa:
        produto:Produto = Produto.create(
            empresa=empresa,
            nome=nome,
            capa=filename,
            descricao=descricao,
            price=float(price),
            categoria=categoria,
        )
        print("Novo Produto Cadastrodado com sucesso")
    else:
        flash("Não foi possivel salvar o produto.")
    

    return redirect(url_for("dashboard.index", name='produto'))
    
@produtos.route("/action/categoria", methods=["POST", "PUT", "DELETE"])
def categoria():
    
    if request.method == "POST":
        nome = request.form.get("categoria", "")
        try:
            Categoria.create(
                nome=nome,
                empresa=1
            )
        except:
            ...
        
    elif request.method == "PUT":
        categoria = Categoria.get_or_none(Categoria.id == request.args.get("id", None))
        if categoria:
            Categoria.delete_instance(categoria)
        
    elif request.method == "DELETE":
        ...
    return redirect(url_for("produtos.index", name='categoria'))


@produtos.delete("/delete/<id>")
def delete(id):
    produto = Produto.get_or_none(Produto.id == id)
    if produto: Produto.delete_instance(produto)
    
    #os.remove()
    
    return redirect(url_for("dashboard.index", name='produto'))


@produtos.before_request
@login_required
def check_out():
    pass



