import os
from flask import (
    Blueprint,
    request,
    url_for,
    redirect,
    session,
    render_template
)

from models import Empresa, Mesa, Produto, Categoria, Pedido, ItenPedido

from utils import converte_moeda

cardapio = Blueprint(
    "cardapio",
    __name__,
    url_prefix="/cardapio",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)


@cardapio.get("/<mesa_uuid>")
def index(mesa_uuid:str):
    
    mesa:Mesa       = Mesa.get_or_none(Mesa.uuid == mesa_uuid)
    empresa:Empresa = Empresa.get_or_none(Empresa.id == mesa.empresa.id)
    
    categoria:Categoria = Categoria.get_or_none(Categoria.id == request.args.get("categoria", None))
    
    if not mesa or not empresa:
        return "mesa não existe"
    
    
    if not mesa.status:
        pedido:Pedido = Pedido.select().where(Pedido.mesa == mesa.id )[-1]
        
        if pedido:
            if pedido.status not in [Pedido.Status.finalizado, Pedido.Status.cancelado]:
                return redirect(url_for("cardapio.pedido", id=pedido.id))
    
    class dados:
        intens_carrinho = 0
        produtos   = []
        categorias = []
        categoria_id = categoria.id if categoria else False
        carrinho     = len([i for i in session.get("carrinho", {})])
        
        nome_restaurante = empresa.nome
        mesa_id  = mesa.uuid
        
    # querys
    query_produtos = Produto.select().where(
        Produto.empresa == empresa
    )
    query_categoria = Categoria.select().where(
        Categoria.empresa == empresa
    )
    
    # filtrar por categoria
    if categoria:
        query_produtos = query_produtos.where(
            Produto.categoria == categoria
        )
    
    for produto in query_produtos:
        produto.price = converte_moeda(produto.price)
        dados.produtos.append(produto)
    
    for categoria in query_categoria:
        dados.categorias.append(categoria)
    
    return render_template("cardapio.index.html", dados=dados)


@cardapio.route("/produto")
def produto():
    
    produto_:Produto = Produto.get_or_none(Produto.id == request.args.get("id", False))
    mesa:Mesa        = Mesa.get_or_none(Mesa.uuid == request.args.get("mesa"))
    
    if not produto_ and not mesa:
        return "Não encontrado."
    
    produto_.price = converte_moeda(produto_.price)
    
    
    return render_template("cardapio.produto.html", produto=produto_, mesa=mesa)


@cardapio.route("/carrinho", methods=["POST", "GET", "DELETE"])
def carrinho():
    
    mesa:Mesa       = Mesa.get_or_none(Mesa.uuid == request.args.get("mesa"))
    empresa:Empresa = Empresa.get_or_none(Empresa.id == mesa.empresa.id)
    carrinho        = session.get("carrinho", {})
    total = 0
    
    if not mesa or not empresa:
        return f"Empresa ou mesa não existe! {mesa} {empresa}"
    
    if request.method == "POST":
        produto:Produto = Produto.get_or_none(Produto.id == request.form.get("produto"))
        try: qtd:int = int(request.form.get("qtd", 1))
        except: qtd = 1
        
        if produto:
            
            carrinho = session.get("carrinho", {})
            if str(produto.id) in carrinho:
                carrinho[str(produto.id)]["qtd"] += qtd
            else:
                carrinho[str(produto.id)] = {
                    "qtd": qtd,
                    "nome": produto.nome,
                    "capa": produto.capa,
                    "id": produto.id,
                    "price": produto.price,
                    "diaplay_price": converte_moeda(produto.price)
                }
                
            
            session["carrinho"] = carrinho
            
        return redirect(url_for("cardapio.index", mesa_uuid=mesa.uuid))
    for id, produto in carrinho.items():
        
        total += float(produto["price"]) * int(produto["qtd"])
    total = converte_moeda(total)
    return render_template("cardapio.carrinho.html", carrinho=carrinho, mesa=mesa, total=total)

@cardapio.delete("/carrinho/delete/<mesa>/<id>")
def carrinho_delete(mesa, id):
    
    carrinho        = session.get("carrinho", {})
    del carrinho[str(id)]
    session["carrinho"] = carrinho
    
    return redirect(url_for("cardapio.carrinho", mesa=mesa))

@cardapio.get("/pedido/new/<mesa>")
def new_pedido(mesa):
    
    mesa:Mesa       = Mesa.get_or_none(Mesa.uuid == mesa)
    if mesa:
        empresa:Empresa = Empresa.get_or_none(Empresa.id == mesa.empresa.id)
    
    carrinho  = session.get("carrinho", {})
    if mesa and empresa:
        pedido:Pedido = Pedido.create(
            empresa=empresa,
            mesa=mesa,
        )
        total = 0
        for id, produto in carrinho.items():
            pd:Produto = Produto.get_or_none(Produto.id == produto["id"])
            if pd:
                ItenPedido.create(
                    empresa=empresa,
                    pedido=pedido,
                    produto=pd,
                    produto_nome=pd.nome,
                    produto_price=pd.price,
                    quantidate=produto["qtd"],
                    subtotal=(pd.price * produto["qtd"])
                )
                total += (pd.price * produto["qtd"])
            
        session["carrinho"] = {}
        pedido.total = total
        mesa.status = False
        mesa.save()
        pedido.save()
        return redirect(url_for("cardapio.pedido", id=pedido.id))
    return "Requisição invalida, escanea o codigo novamente"

@cardapio.get("/pedido/<id>")
def pedido(id):
    
    pedido_:Pedido = Pedido.get_or_none(Pedido.id == id)
    if not pedido_:
        return "Pedido Não encontrado, ou pedido finalizado"
    
    if pedido_.status in [Pedido.Status.finalizado, Pedido.Status.cancelado]:
        return redirect(url_for("cardapio.index", mesa_uuid = pedido_.mesa.uuid))
    
    class dados:
        mesa_pedido   = pedido_.mesa.nome
        total         = converte_moeda(pedido_.total)
        status_pedido = pedido_.status
        
        lista_produtos = []
    
    if pedido_:
        
        for produto in ItenPedido.select().where(ItenPedido.pedido == pedido_):
            
            produto.produto_price = converte_moeda(produto.produto_price)
            produto.subtotal      = converte_moeda(produto.subtotal)
            
            
            dados.lista_produtos.append(produto)
        
        return render_template("cardapio.pedido.html", dados=dados)
    
    return "O pedido não existe ou já foi finalizado"


