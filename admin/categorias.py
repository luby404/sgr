from .base import Model

from models import Usuario, Empresa, Categoria
from flask_login import current_user

current_user:Usuario

class CategoriaAdmin(Model):
    roles       = ["gestor", "admin"]
    
    column_editable_list = ["cardapio", "is_ative"]
    can_delete = False
    
    column_list = ["nome", "cardapio",  "is_ative", "criado_em"]
    column_searchable_list = ["nome"]
    
    
    def set_roles(self):
        if current_user.user_type == "gestor":
            self.can_delete = False
        
        return super().set_roles()
    
  