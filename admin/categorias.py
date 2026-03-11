from .base import Model

from models import Usuario, Empresa, Categoria
from flask_login import current_user

current_user:Usuario

class CategoriaAdmin(Model):
    column_list = ["nome", "cardapio", "is_ative", "criado_em"]
    roles       = ["empresa_gestor", "empresa_admin"]
    
    column_editable_list = ["cardapio", "is_ative"]
    can_delete = False
    
    column_searchable_list = ["nome"]
    
    
    def set_roles(self):
        if current_user.user_type == "empresa_gestor":
            self.can_delete = False
        
        return super().set_roles()
    
    def on_model_change(self, form, model:Categoria, is_created):
        if is_created:
            model.empresa = current_user.empresa
            
        return super().on_model_change(form, model, is_created)
