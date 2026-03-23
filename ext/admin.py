from flask_admin import Admin
from flask import Flask, url_for

from flask_admin.theme import Bootstrap4Theme
from flask_admin.menu import MenuLink, MenuDivider
from models import (
    Usuario,
    Empresa,
    Pagamento,
    Assinatura,
    Plano,
    Produto, Categoria, Mesa, Pedido, ItenPedido
    
)
from admin.base import Link
from admin.usuarios import UsuarioAdmin
from admin.empresa import EmpresaAdmin
from admin.assinatura import AssinaturaAdmin
from admin.planos import PlanosAdmin
from admin.pagamentos import PagamentoAdmin
from admin.categorias import CategoriaAdmin
from admin.mesas import MesaAdmin
from admin.pedidos import PedidoAdmin

# empresa
from admin.produtos import ProdutosAdmin

#lux, pulse, journal

admin = Admin(
    name="Painel Adminstrativo",
    theme=Bootstrap4Theme(
        swatch="journal", 
        fluid=True,
    )
)

class categoria_admin:
    cardapio = "Cardapio"
    operacao = "Operação"
    

admin.add_views(
    UsuarioAdmin(Usuario),
    EmpresaAdmin(Empresa),
    
    PlanosAdmin(Plano),
    AssinaturaAdmin(Assinatura),
    PagamentoAdmin(Pagamento),
    
    CategoriaAdmin(Categoria, category=categoria_admin.cardapio),
    ProdutosAdmin(Produto, category=categoria_admin.cardapio),
    #
    MesaAdmin(Mesa, category=categoria_admin.operacao),
    PedidoAdmin(Pedido, category=categoria_admin.operacao)
    

)
auth_link = Link(name="Sair", url="/auth/logout")
auth_link.roles = ["admin", "empresa_admin", "empresa_gestor"]

dashboard_link = Link(name="Dashboard", url="/dashboard/home")
dashboard_link.roles = ["empresa_admin", "empresa_gestor"]


admin.add_links(
    dashboard_link,
    auth_link,
)


def init_admin(app: Flask):
    admin.init_app(app)
    