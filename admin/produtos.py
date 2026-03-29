import os
from .base import Model
from utils import BASE_DIR
from models import Produto, Empresa, Categoria, Usuario


from flask_admin.form.upload import ImageUploadField

from markupsafe import Markup
from flask import url_for

from flask_login import current_user

current_user:Usuario

class ProdutosAdmin(Model):
    form_excluded_columns = ["capa",  "estoque", "criado_em", "atualizado_em", "is_ative", "empresa", "cardapio"]
    column_list           = ["capa", "nome", "categoria", "price", "cardapio", "estoque"]
    roles                 = ["gestor", "admin"]
    column_default_sort = ("categoria", True)
    column_editable_list = ["cardapio", "categoria", "price", "nome"]
    
    
    form_extra_fields = {
        "capa": ImageUploadField(
            label="Imagen do produto",
            base_path=os.path.join(BASE_DIR, "produtos"),
        )
    }
    
    def _imagem(view, context, model, name):
        if not model.capa:
            return ""

        url = url_for("static", filename=f"uploads/produtos/{model.capa}")

        return Markup(
            f"""
            <img src="{url}"
            style="
                height: 80px;
                object-fit:cover;
                border-radius:8px;
                border:1px solid #ddd;
            ">
            """
        )

    column_formatters = {
        "capa": _imagem
    }
   