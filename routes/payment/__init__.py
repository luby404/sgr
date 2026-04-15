import os
from flask import *

from utils import converte_moeda
from flask_login import login_required, current_user

from models import Pedido, Usuario, Empresa, Produto, ItenPedido

from print_esp import Print



payment = Blueprint(
    "payment",
    __name__,
    url_prefix="/payment",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)

prt = Print()

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
            telefone = "931617941"
            nome = "Cramer"
            
            pagamento = True if str(tipo) == "1" else False
            
            
            for produto in pedido.produtos.select():
                produto:ItenPedido = produto
                
                total += float(produto.subtotal)
                
                #produto.produto_price = converte_moeda(produto.produto_price)
                #produto.subtotal     = converte_moeda(produto.subtotal)
                
                # ("cocacola", 2, 100)
                produtos.append(
                    [
                        produto.produto_nome,
                        produto.quantidate,
                        produto.produto_price,
                    ]
                )
                
            
            # imprimir recibo
            prt.print_recibo_pedido(produtos, total=converte_moeda(total), mesa=mesa, pedido=pedido)
        return "recibo imprimido com sucesso!"
            
        #return render_template("print.html", dados=dados)


@payment.get("/recibo/mesa/<id>")
def recibo_mesa(id):
    
    url = request.url_root + url_for("cardapio.reck_mesa", id=id)
    prt.print_recibo_qr_mesa(url, "1")
    
    
    return redirect("/admin/mesa/")

@payment.before_request
@login_required
def check_out():
    pass