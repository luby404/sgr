from .base import Model

from models import Usuario, Empresa, Categoria, Mesa
from flask_login import current_user
from flask import url_for
from markupsafe import Markup

current_user:Usuario



class MesaAdmin(Model):
    column_list = ["nome", "status", "criado_em", "uuid", "link"]
    roles       = ["gestor", "admin"]
    
    column_editable_list = ["nome", "status"]
    
    form_excluded_columns = ["criado_em", "atualizado_em", "empresa", "uuid",]
    
    
    
    
    def set_roles(self):
        if current_user.user_type == "gestor":
            self.can_delete = False
        
        return super().set_roles()
    
    
    def _lisk_print(view, context, model:Mesa, name):
        url = url_for("payment.recibo_mesa", id=model.id)
        return Markup(f"<a href='{url}' >Imprimir</a>")
    
    
    column_formatters = {
        "link": _lisk_print
    }
    
