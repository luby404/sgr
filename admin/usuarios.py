from .base import Model
from flask_login import current_user
from models import Usuario

from wtforms.fields import PasswordField

from flask_admin import expose

class UsuarioAdmin(Model):
    form_excluded_columns = ["criado_em", "atualizado_em", "empresa"]
    
    column_list = ["nome", "email", "user_type", "criado_em"]
    roles       = ["admin"]
    
    form_extra_fields = {
        "senha": PasswordField(label="Senha")
    }
    
    
    def on_model_change(self, form, model:Usuario, is_created):
        
        if is_created:
            model.set_password(model.senha)
        
        return super().on_model_change(form, model, is_created)

    