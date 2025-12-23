import os
from flask import (
    Blueprint,
    request,
    url_for,
    redirect,
    session,
    render_template
)


from models import Pedido, Comanda, Venda, ItemPedido
from ext.uitls import converte_moeda

from flask_login import current_user,login_required

dashboard = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)



@dashboard.get("/")
@dashboard.get("/home/")
def home():
    
    _pedidos = Pedido.select()
    
    vendas:Venda = Venda.select().where(
        Venda.vendedor == current_user.id
    )
    
    class Dados:
        pedidos    = _pedidos.count()
        concluidos = _pedidos.where(Pedido.status == "finalizado").count()
        pendentes  = _pedidos.where(Pedido.status == "pendente").count()
        canceladas = _pedidos.where(Pedido.status == "cancelado").count()
        
        comandas   = Comanda.select().where(Comanda.status == "aberta").count()
        vendas_dia = converte_moeda( sum( [ n.valor for n in vendas ] ) )
    
    return render_template("dh.home.html", dados=Dados)


@dashboard.get("/pedidos/")
def pedidos():

    tipos = [k for k,v in Pedido.status.choices]
    tipo  = request.args.get("tipo", "").strip()
    
    if tipo not in tipos:
        tipo = "pendente"
    
    class Dados:
        tipos_pedido = tipos
        pedidos = [p for p in Pedido.select().where(Pedido.status == tipo)]
        
        
        for c in pedidos: c.sub_total = converte_moeda(sum([float(i.preco) * float(i.quantidade) for i in c.itens.select()]))
        
        #   pedidos.reverse()
        
    return render_template("dh.pedidos.html", dados=Dados)



@dashboard.before_request
@login_required
def check_auth():
    #if current_user.is_authenticated
    ...
