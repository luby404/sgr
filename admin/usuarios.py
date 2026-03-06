from .base import Model

class UsuarioAdmin(Model):
    form_excluded_columns = ["criado_em", "atualizado_em", "empresa"]
    
    column_list = ["nome", "email", "user_type", "criado_em"]



