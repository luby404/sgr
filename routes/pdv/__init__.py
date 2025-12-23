import os
from flask import (
    Blueprint,
    request,
    url_for,
    redirect,
    session,
    sessions,
    render_template,
    flash
)


from models import (
    Produtos,
    Categorias,
    Settings,
    Comanda,
    Pedido,
    ItemPedido,
    Venda,
    Usuarios,
)

from flask_login import current_user, login_required

from ext.uitls import converte_moeda, CARRINHO



pdv = Blueprint(
    "pdv",
    __name__,
    url_prefix="/pdv",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)

@pdv.route("/new", methods=["GET", "POST"])
def new():
    # gera nova comanda
    class Dados:
        comandas = Comanda.select().where(
            Comanda.is_ative == True and Comanda.status == "aberta"
        )
        
    
    if request.method == "POST":
        comanda_id = request.form.get("comanda", "").strip()
        comanda:Comanda = Comanda.get_or_none(Comanda.id == comanda_id)
        if comanda.status == "aberta":
            pedido = Pedido.create(comanda=comanda)
            comanda.status = "fechada"
            comanda.save()
            
            return redirect(url_for("pdv.pedido", pedido=pedido.id))
        
    return render_template("pdv.modal_selct.html", dados=Dados)

@pdv.route("/pedido",  methods=["GET"])
def pedido():
    
    categoria:Categorias  = Categorias.get_or_none(Categorias.id == request.args.get("cate", "").strip())
    pedido_id:Pedido      = Pedido.get_or_none(Pedido.id == request.args.get("pedido", "").strip())
    
    if not pedido_id: return "Pedido Não existe"
        
    if not categoria:
        categoria = "all"
    
    class Dados:
        status   = True if pedido_id.status != "pendente" else False
        comanda  = None
        carrinho = ItemPedido.select().where(
            ItemPedido.pedido == pedido_id
        )
        
        for c in carrinho: c.display_price = converte_moeda(c.preco)
        
        comanda = 0
        
        # pedido infos
        pedido:Pedido = pedido_id
        
        
                
        categorias = [
            cate
            for cate in Categorias.select().where(
                Categorias.is_ative == True
            )
        ]
        produtos   = [
            produto
            for produto in Produtos.select().where(
                (Produtos.is_ative == True) &
                (Produtos.quantidade >= 1)
            )
        ]
        
        # subistituir o campo valor por valor formatado ...
        for n in range(0, len(produtos)): produtos[n].preco_venda = converte_moeda(produtos[n].preco_venda)
        
        if categoria != "all":
            produtos = list(filter(lambda e: e.categoria == categoria, produtos))
        
        _total = sum([float(i.preco) * float(i.quantidade) for i in pedido.itens.select()])
        _taxa       = 0.1
        
        
        sub_total  = converte_moeda(_total)
        taxa = _taxa * 100
        total      = converte_moeda( float((_total * _taxa) + _total)  )
        
        total_itens = pedido_id.itens.select().count()
    
    
    return render_template("pdv.pedido.html", dados=Dados)

# actions
@pdv.route("/add_carrinho")
def add_carrinho():
    
    
    produto_id = request.args.get("produto", "").strip()
    pedido_id  = request.args.get("pedido", "").strip()
        
    produto:Produtos = Produtos.get_or_none(Produtos.id == produto_id)
    pedido:Pedido    = Pedido.get_or_none(Pedido.id == pedido_id)
    
    if produto and pedido:
        iten_pedido = ItemPedido.get_or_none((ItemPedido.pedido == pedido.id) & (ItemPedido.produto == produto.id))
       
        if iten_pedido:
            # atualizar dados do produto
            iten_pedido.quantidade += 1
            iten_pedido.save()
        else:
            iten_pedido = ItemPedido.create(
                pedido=pedido,
                produto=produto,
                quantidade=1,
                preco=produto.preco_venda
            )        
        pedido.produtos  += 1
        pedido.save()
    else:
        return "Produto não existe"
        
    
    return redirect(url_for("pdv.pedido", pedido=pedido.id))

@pdv.route("/delete_carrinho")
def delete_carrinho():
    
    
    produto_id = request.args.get("produto", "").strip()
    pedido_id  = request.args.get("pedido", "").strip()
        
    pedido:Pedido    = Pedido.get_or_none(Pedido.id == pedido_id)
    
    if pedido:
        iten:ItemPedido = ItemPedido.get_by_id(produto_id)
        pedido.produtos  -= iten.quantidade
        pedido.save()
        
        ItemPedido.delete_instance(iten)
        
    return redirect(url_for("pdv.pedido", pedido=pedido.id))


@pdv.route("/finalizar", methods=["GET", "POST"])
def finalizar():
    
    #current_user: Usuarios = current_user
    
    pedido:Pedido = Pedido.get_or_none(Pedido.id == request.args.get("pedido", "").strip())
    
    if pedido:
        carrinho = ItemPedido.select().where(
            ItemPedido.pedido == pedido.id
        )
        
        taxa      = 0.1
        sub_total = sum([float(i.preco) * float(i.quantidade) for i in pedido.itens.select()])
        total     = float( (sub_total * taxa) + sub_total )
        troco  = 0
        
        if request.method == "POST" and pedido.status == "pendente":
            user:Usuarios = Usuarios.get_or_none(Usuarios.id == current_user.id)
            
            
            venda:Venda = Venda.create(
                caixa=1,
                vendedor=user,
                pedido=pedido,
                valor=total
            )
            
            pedido.fechado_em = venda.data
            pedido.status     = "finalizado"
            comanda:Comanda = Comanda.get_or_none(Comanda.id == pedido.comanda.id)
            if comanda:
                comanda.status = "aberta"
                comanda.save()
            pedido.save()
            
            
            return redirect(url_for("pdv.recibo", pedido=pedido.id, venda=venda.id))
            
            
        class Dados:
            pedido_id   = pedido.id
            valor_total = converte_moeda(total)
            
        
        return render_template("pdv.finalizar.html", dados=Dados)
    else:
        return "pedido não existe"


@pdv.get("/cancel")
def cancel_pedido():
    
    pedido:Pedido      = Pedido.get_or_none(Pedido.id == request.args.get("pedido", "").strip())
    if not pedido:
        return "Pedido Não exixte"
    
    if pedido.status == "pendente": 
        pedido.status = "cancelado"
        comanda:Comanda = Comanda.get_or_none(Comanda.id == pedido.comanda.id)
        if comanda:
            comanda.status = "aberta"
            comanda.save()
    
    pedido.save()
    
    
    return redirect(url_for("dashboard.pedidos"))

@pdv.get("/detalhes")
def detalhes():
    
    pedido:Pedido = Pedido.get_or_none(Pedido.id == request.args.get("pedido", "").strip())
    venda = None
    if pedido:
        venda:Venda   = Venda.get_or_none(Venda.pedido  == pedido.id)
    
    if pedido and venda:
        return redirect(url_for("pdv.recibo", pedido=pedido.id, venda=venda.id))

    return "Pedido Não existe"

@pdv.route("/recibo")
def recibo():
    
    pedido:Pedido = Pedido.get_or_none(Pedido.id == request.args.get("pedido", "").strip())
    venda:Venda   = Venda.get_or_none(Venda.id   == request.args.get("venda", "").strip())
    if pedido and venda:
        carrinho = ItemPedido.select().where(
            ItemPedido.pedido == pedido.id
        )
        
        _taxa      = 0.1
        _sub_total = sum([float(i.preco) * float(i.quantidade) for i in pedido.itens.select()])
        _total     = float( (_sub_total * _taxa) + _sub_total )
        troco  = 0
        
        
        class Dados:
            data         = pedido.fechado_em
            pedido_id    = pedido.id
            produtos     = carrinho 
            valor_total  = converte_moeda(_total)
            comanda      = pedido.comanda.codigo
            taxa         = int(_taxa * 100)
            valor_pago   = converte_moeda(0)
            sub_total    = converte_moeda(_sub_total)
            troco        = converte_moeda(0)
            
            
            for p in produtos:
                p._subtotal = float(p.preco * p.quantidade)
                p.subtotal  = converte_moeda(p._subtotal)
                p.preco     = converte_moeda(float(p.preco))
        return render_template("pdv.recibo.html", dados=Dados)
    else:
        return "pedido não existe"