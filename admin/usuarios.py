from .base import Model
from flask_login import current_user
from models import Usuario

from wtforms.fields import PasswordField, SelectField

from flask_admin import expose

class UsuarioAdmin(Model):
    form_excluded_columns = ["criado_em", "atualizado_em", "empresa"]
    
    column_list = ["nome", "email", "user_type", "criado_em"]
    roles       = ["admin", "empresa_admin", "empresa_gestor"]
    
    form_extra_fields = {
        "senha": PasswordField(label="Senha"),
    }
    
    def set_roles(self):
        
        rule = self.user.user_type
        
        self.form_extra_fields["user_type"] = SelectField(label="Tipo de usuario", choices=[
            ("nome", "Nome")
        ])  
        
        return super().set_roles()
    
    def on_model_change(self, form, model:Usuario, is_created):
        
        if is_created:
            model.empresa = current_user.empresa
            model.set_password(model.senha)
        
        return super().on_model_change(form, model, is_created)

    