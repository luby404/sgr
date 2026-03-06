from .base import Model
from flask import flash
from models import Usuario, Empresa
from werkzeug.security import generate_password_hash

class EmpresaAdmin(Model):
    column_list = ["nome", "email", "nif", "telefone", "is_ative"]
    
    def after_model_change(self, form, model:Empresa, is_created):
        
        if is_created:
            Usuario.create(
                nome=model.nome,
                email=model.email,
                senha=generate_password_hash("admin"),
                user_type=Usuario.roles.empresa
            )
            flash(f"Super Usuario de {model.nome} criado com sucesso!")
        
        return super().after_model_change(form, model, is_created)



