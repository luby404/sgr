from flask_admin import Admin
from flask import Flask, url_for

from flask_admin.theme import Bootstrap4Theme
from flask_admin.menu import MenuLink, MenuDivider
from models import (
    Usuario,
    Empresa,
    Estoque,
    Produto, Categoria, Mesa, Pedido, ItenPedido
    
)
from admin.base import Link
from admin.usuarios import UsuarioAdmin
from admin.categorias import CategoriaAdmin
from admin.mesas import MesaAdmin
from admin.pedidos import PedidoAdmin
from admin.estoque import EstoqueAdmin
from admin.relatorio import RelatoriosAdmin

# empresa
from admin.produtos import ProdutosAdmin

#lux, pulse, journal

admin = Admin(
    name="Painel Adminstrativo",
    theme=Bootstrap4Theme(
        swatch="journal", 
        #fluid=True,
    )
)

class categoria_admin:
    cardapio = "Cardapio"
    operacao = "Operação"
    

admin.add_views(
    UsuarioAdmin(Usuario),
    
    
    CategoriaAdmin(Categoria, category=categoria_admin.cardapio),
    ProdutosAdmin(Produto, category=categoria_admin.cardapio),
    #
    MesaAdmin(Mesa, category=categoria_admin.operacao),
    PedidoAdmin(Pedido, category=categoria_admin.operacao),
    EstoqueAdmin(Estoque, category=categoria_admin.operacao),
    
    RelatoriosAdmin(
        name="Relátorios",
        category=categoria_admin.operacao
    )

)



admin.add_links(
    Link(name="Dashboard", url="/home"),
    Link(name="Sair", url="/auth/logout"),
)


def init_admin(app: Flask):
    admin.init_app(app)
    