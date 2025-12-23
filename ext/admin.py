import os
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from flask_admin.form import ImageUploadField

from models import (
    Usuarios, Categorias, Produtos,
    Fornecedor, Estoque,
    Mesa, Comanda,
    Pedido, ItemPedido,
    Caixa, Venda,
    Settings
)


uploads = os.path.join(os.getcwd(), "static", "uploads")
os.makedirs(uploads, exist_ok=True)


class BaseModelView(ModelView):
    column_exclude_list = (
        "senha", "criado_em", "atualizado_em", "id"
    )

    form_excluded_columns = (
        "senha", "criado_em", "atualizado_em", "id", "mesa"
    )

    edit_modal = True
    create_modal = True
    can_view_details = True


class UsuarioAdmin(BaseModelView):
    column_list = ("nome", "email", "user_type")



class CategoriasAdmin(BaseModelView):
    column_list = ("nome",)


class ProdutosAdmin(BaseModelView):
    column_list = (
        "nome", "categoria",
        "quantidade", "preco_venda",
        "estoque_minimo"
    )

    form_extra_fields = {
        "capa_produto": ImageUploadField(
            label="Imagem do Produto",
            allowed_extensions=["png", "jpg", "jpeg", "webp"],
            base_path=uploads
        )
    }

class FornecedorAdmin(BaseModelView):
    column_list = ("nome", "telefone")


class EstoqueAdmin(BaseModelView):
    column_list = (
        "produto", "movimento",
        "quantidade", "preco_compra",
        "data"
    )

    def on_model_change(self, form, model: Estoque, is_created):
        produto = model.produto

        if is_created:
            if model.movimento == "entrada":
                produto.quantidade += model.quantidade

            elif model.movimento == "saida":
                produto.quantidade -= model.quantidade

            elif model.movimento == "ajuste":
                produto.quantidade = model.quantidade

        produto.save()
        return super().on_model_change(form, model, is_created)

class MesaAdmin(BaseModelView):
    column_list = ("numero", "status")


class ComandaAdmin(BaseModelView):
    column_list = (
        "id", "codigo", #"mesa",
        "status"
    )
    

class PedidoAdmin(BaseModelView):
    column_list = (
        "id", "comanda", "produtos",
        "status", "aberto_em", "fechado_em"
    )

class ItemPedidoAdmin(BaseModelView):
    column_list = (
        "pedido", "produto",
        "quantidade", "preco"
    )



class CaixaAdmin(BaseModelView):
    column_list = (
        "nome", "status",
        "saldo_inicial", "saldo_atual",
        "aberto_em", "fechado_em"
    )


class VendaAdmin(BaseModelView):
    column_list = (
        "comanda", "vendedor",
        "valor", "data"
    )


class SettingsAdmin(BaseModelView):
    column_list = ("nome", "nif", "taxa")


def init_admin(app):
    admin = Admin(app, name="Painel de Gestão")

    class cat:
        estoque = "Estoque"
        atendimento = "Atendimento"
        sistema = "Sistema"

    admin.add_views(
        UsuarioAdmin(Usuarios, category=cat.sistema),

        CategoriasAdmin(Categorias, category=cat.estoque),
        ProdutosAdmin(Produtos, category=cat.estoque),
        FornecedorAdmin(Fornecedor, category=cat.estoque),
        EstoqueAdmin(Estoque, name="Movimentações", category=cat.estoque),

        #MesaAdmin(Mesa, category=cat.atendimento),
        ComandaAdmin(Comanda, category=cat.atendimento),
        PedidoAdmin(Pedido, category=cat.atendimento),
        ItemPedidoAdmin(ItemPedido, category=cat.atendimento),

        #CaixaAdmin(Caixa, category=cat.sistema),
        VendaAdmin(Venda, category=cat.sistema),

        SettingsAdmin(Settings, category=cat.sistema),
    )


