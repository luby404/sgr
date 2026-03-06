
# regras de usuario
ROLES = {
    "admin": [],
    "caixa": ["pedido.read", "pedido.edite"],
    "gerente": ["pedidos.add", "pedidos.edite", "pedidos.delete"]
}