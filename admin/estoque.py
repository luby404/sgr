from .base import Model
from flask import flash
from models import Usuario, Estoque, Produto

from flask_login import current_user

current_user:Usuario

class EstoqueAdmin(Model):
    
    column_list = ["produto", "quantidade", "tipo", "criado_em"]
    
    can_delete = False
    can_edit   = False
    
    def on_model_change(self, form, model:Estoque, is_created):
        
        if is_created:
            model.usuario = current_user.id
            produto:Produto = Produto.get_or_none(Produto.id == model.produto.id)
            if produto:
                if model.tipo == "entrada":
                    produto.estoque += int(model.quantidade)
                elif model.tipo == "saida":
                    produto.estoque -= int(model.quantidade)
                elif model.tipo == "ajuste":
                    produto.estoque = int(model.quantidade)
                produto.save()
        return super().on_model_change(form, model, is_created)
    