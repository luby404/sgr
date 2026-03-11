from .base import Model
from flask import flash
from models import Usuario, Empresa
from werkzeug.security import generate_password_hash

from flask_login import current_user

class EmpresaAdmin(Model):
    column_list = ["nome", "email", "nif", "telefone", "is_ative"]
    roles       = ["admin"]
    
    """def set_roles(self):
        # modificar regras
        if self.user.user_type == "empresa_admin":
            self.can_create = False
            self.can_delete = False
            
        return super().set_roles()"""
    
    def after_model_change(self, form, model:Empresa, is_created):
        
        if is_created:
            Usuario.create(
                nome=model.nome,
                email=model.email,
                senha=generate_password_hash("admin"),
                user_type=Usuario.roles.empresa,
                empresa=model
            )
            flash(f"Super Usuario de {model.nome} criado com sucesso!")
        
        return super().after_model_change(form, model, is_created)

    
    def get_query(self):

        query = super().get_query()

        if current_user.user_type == "empresa_admin":
            query = query.where(
                Empresa.id == current_user.empresa
            )            
        return query

