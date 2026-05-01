import os
from flask import *

from .views import pages

from models import Produto, Categoria, Usuario, Mesa, ItenPedido, Pedido, Empresa

from flask_login import current_user, login_required


from utils import converte_moeda

from datetime import datetime, timedelta, date, time

current_user:Usuario


dashboard = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)

@dashboard.get("/")
@dashboard.route("/<name>", methods=["GET", "POST", "DELETE", "PUT"])
def index(name=None):
    if not name:
        name = "home"
    
    
    categoria:Categoria = Categoria.get_or_none(Categoria.id == request.args.get("categoria", None))
    
    status_pedido:Pedido.Status = Pedido.Status
    class Dados:
        
        # carrinho
        carrinho = session.get("carrinho", {})
        total = converte_moeda(sum([
            float(produto["price"]) * float(produto["qtd"]) 
            for id, produto in carrinho.items()
        ]))
        
        user_name = current_user.nome
        
        # dashboard
        pedidos_pendentes     = 0
        pedidos_entreges      = 0
        pedidos_em_preparacao = 0
        pedidos_finalizados   = 0
        vendas_do_dia         = 0
        
        
        view = ""
        produtos_pedido = []
        pedido_total = 0
        pedido_mesa = Pedido
        status = request.args.get("status", status_pedido.pendente)
        
        
        produtos = []
        
        categorias = []
        pedidos    = [p for p in Pedido.select().where(
            (Pedido.status == status)
        )]
        
        alert = True if len(pedidos) > 0 else False
        
        #pedidos.reverse()
        
        pedido_status = (status_pedido.pendente, status_pedido.preparacao, status_pedido.entregue, status_pedido.finalizado, status_pedido.cancelado)
        
        if categoria:
            categoria_id = categoria.id
        else:
            categoria_id = categoria
    
    
    if name in pages:
        
        if name == "home":
            # cacular dados de resumo
            data_hoje = datetime.now().date()
            start_data = datetime.combine(data_hoje, time.min)
            and_data   = datetime.combine(data_hoje, time.max)
            
            
            query_pedidos = Pedido.select().where(
                (Pedido.criado_em >= start_data) &
                (Pedido.criado_em <= and_data) &
                (Pedido.usuario == Usuario.get_or_none(Usuario.id == current_user)) # buscar por usuario
            )
            query_finalizados = query_pedidos.where(Pedido.status == status_pedido.finalizado)
            
            Dados.pedidos_pendentes     = query_pedidos.where(Pedido.status == status_pedido.pendente).count()
            Dados.pedidos_em_preparacao = query_pedidos.where(Pedido.status == status_pedido.preparacao).count()
            Dados.pedidos_entreges      = query_pedidos.where(Pedido.status == status_pedido.entregue).count()
            Dados.pedidos_finalizados   = query_finalizados.count()
            
            Dados.vendas_do_dia = converte_moeda( sum(
                [float(i.total) for i in query_finalizados]
            ) )
        
        mesa:Mesa = Mesa.get_or_none(Mesa.id == request.args.get("mesa", None))
        if name == "view_pedido" and mesa:
            pedido:Pedido = Pedido.select().where(Pedido.mesa == mesa)[-1]
            if pedido:
                #if pedido.status not in [Pedido.Status.finalizado, Pedido.Status.cancelado]:
                    Dados.pedido_mesa = pedido
                    for produto in ItenPedido.select().where(ItenPedido.pedido == pedido):
                        produto.price = converte_moeda(produto.produto_price)
                        Dados.produtos_pedido.append(produto)
                        Dados.pedido_total += produto.subtotal
            
                    print("iten do produto encontrado.")
                    Dados.pedido_total = converte_moeda(Dados.pedido_total)
                    
        if name == "pos":
            
            query_produtos = Produto.select().where(
                Produto.cardapio
            )
            # filtrar por categoria
            if categoria:
                query_produtos = query_produtos.where(
                    Produto.categoria == categoria
                )
            
            for produto in query_produtos:
                produto.price = converte_moeda(produto.price)
                Dados.produtos.append(produto)
                
                
            Dados.categorias = Categoria.select()
            
        Dados.view =  render_template(pages[name], dados=Dados)
    else:
        return render_template("404.html")
    
    if request.args.get("view", False):
        return Dados.view

    return render_template("dh.index.html", dados=Dados)

@dashboard.post("/update_pedido/<id>")
def update_pedido(id):
    pedido:Pedido  = Pedido.get_or_none(Pedido.id == id)
     
    new_status    = request.form.get("status_update", Pedido.Status.pendente)
    if pedido:
        pedido.status = new_status
        mesa:Mesa = Mesa.get_or_none(Mesa.id == pedido.mesa.id)
        if mesa:
            if pedido.status in [Pedido.Status.finalizado, Pedido.Status.cancelado]:
                mesa.status = True
                pedido.usuario = current_user
            else:
                mesa.status = False
            mesa.save()
        # voltar o estoque
        for itenpedido in pedido.produtos.select():
            itenpedido:ItenPedido = itenpedido
            if pedido.status == Pedido.Status.cancelado:
                produto:Produto = Produto.get_or_none(Produto.id == itenpedido.produto)
                if produto:
                    produto.estoque = int(produto.estoque) + int(itenpedido.quantidate)
                    produto.save()
            
        pedido.save()
        return redirect(url_for("dashboard.index", mesa=pedido.mesa.id, name="view_pedido"))
    return "Pedido Não encontrado."

@dashboard.get("/check_pedidos")
def check_pedido():
    class dados:
        pedidos = Pedido.select().where(
            (Pedido.status == Pedido.Status.pendente)
        )
        status = True if pedidos.count() > 0 else False        
    
    return stream_template("dh.produtos_list.html", dados=dados)

@dashboard.before_request
@login_required
def check_out():
    pass



