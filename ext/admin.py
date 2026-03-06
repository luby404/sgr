from flask import Flask
from flask_admin import Admin

from flask_admin.theme import Bootstrap4Theme

from models import (
    Usuario,
    Empresa,
    Pagamento,
    Assinatura,
    Plano
    
)

from admin.usuarios import UsuarioAdmin
from admin.empresa import EmpresaAdmin
from admin.assinatura import AssinaturaAdmin
from admin.planos import PlanosAdmin
from admin.pagamentos import PagamentoAdmin

#lux

admin = Admin(
    name="Painel Adminstrativo",
    theme=Bootstrap4Theme(
        swatch="lux", 
        fluid=False,
    )
)

admin.add_views(
    UsuarioAdmin(Usuario),
    EmpresaAdmin(Empresa),
    PlanosAdmin(Plano),
    AssinaturaAdmin(Assinatura),
    PagamentoAdmin(Pagamento)
    

)

def init_admin(app: Flask):
    admin.init_app(app)