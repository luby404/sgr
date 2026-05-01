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
    msg = dict(
        msg="Pedido impresso com sucesso!",
        status=False
    )
    
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
            try:
                prt.print_recibo_pedido(produtos, total=converte_moeda(total), mesa=mesa, pedido=pedido)
                msg["status"] = True
            except:
                msg["msg"] = "Não foi possivel imprimir o recibo"
            
            
        return msg
            
        #return render_template("print.html", dados=dados)


@payment.get("/recibo/mesa/<id>")
def recibo_mesa(id):
    
    url = request.url_root + url_for("cardapio.reck_mesa", id=id)
    prt.print_recibo_qr_mesa(url, "1")
    

    return redirect("/admin/mesa/")


@payment.get("/finalizar_pos")
def pos_finalizar():
    total = 0
    carrinho = session.get("carrinho_pos", {})
    
    for key, iten in carrinho.items():
        total += float(float(iten["price"]) * int(iten["qtd"]))
    
    pedido_pos:Pedido = Pedido.create(
        usuario=current_user,
        status=Pedido.Status.finalizado,
        total=total
    )
    
    for key, iten in carrinho.items():
        produto:Produto = Produto.get_or_none(Produto.id == key)
        if produto:
             ItenPedido.create(
                 pedido=pedido_pos,
                 produto=produto,
                 produto_nome=produto.nome,
                 produto_price=produto.price,
                 quantidate=int(iten["qtd"]),
                 subtotal=float(int(iten["qtd"] * float(produto.price)))
                 
             )
        produto.estoque = int(produto.estoque) - int(iten["qtd"])
        produto.save()
        
    if pedido_pos:
        tipo = 1
        class dados:
            produtos = []
            mesa = ""
            num_pedido = pedido_pos.id
            total = 0
            data = pedido_pos.fechado_em.strftime("%d-%m-%Y %H:%M")
            telefone = "931617941"
            nome = "Cramer"
            
            
            
            
            for produto in pedido_pos.produtos.select():
                produto:ItenPedido = produto
                
                total += float(produto.subtotal)
                
                produtos.append(
                    [
                        produto.produto_nome,
                        produto.quantidate,
                        produto.produto_price,
                    ]
                )
                
            
            # imprimir recibo
            try:
                
                prt.print_recibo_pedido(produtos, total=converte_moeda(total), mesa=mesa, pedido=pedido_pos)
                prt.print_recibo_pedido(produtos, cozinha=True, total=converte_moeda(total), mesa=mesa, pedido=pedido_pos)
                session["carrinho_pos"] = {}
            except:
                "Não foi possivel imprimir o recibo"
            
    return redirect(url_for("cardapio.carrinho_pos"))
    



@payment.before_request
@login_required
def check_out():
    pass