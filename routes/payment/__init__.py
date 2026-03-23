import os
from flask import *

from utils import converte_moeda
from flask_login import login_required, current_user

from models import Pedido, Usuario, Empresa

payment = Blueprint(
    "payment",
    __name__,
    url_prefix="/payment",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)


@payment.get("/recibo/<id>")
def recibo(id):
    tipo = request.args.get("type", None)
    
    pedido:Pedido = Pedido.get_or_none(Pedido.id == id)
    if pedido:
        class dados:
            produtos = []
            mesa = pedido.mesa.nome
            num_pedido = pedido.id
            total = 0
            data = pedido.fechado_em.strftime("%d-%m-%Y %H:%M")
            telefone = pedido.empresa.telefone
            nome = pedido.empresa.nome
            
            pagamento = True if str(tipo) == "1" else False
            
            
            for produto in pedido.produtos.select():
                total += float(produto.subtotal)
                
                produto.produto_price = converte_moeda(produto.produto_price)
                produto.subtotal = converte_moeda(produto.subtotal)
                
                produtos.append(produto)
            
        return render_template("print.html", dados=dados)

@payment.before_request
@login_required
def check_out():
    empresa:Empresa = Empresa.get_or_none(Empresa.id == current_user.empresa)
    if not empresa:
        return redirect(url_for("auth.login"))