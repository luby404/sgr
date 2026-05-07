import os

BASE_DIR = os.path.join(os.getcwd(),"static", "uploads")

if not os.path.exists(BASE_DIR): os.mkdir(BASE_DIR)


# regras de usuario
ROLES = {
    "admin": [],
    "caixa": ["pedido.read", "pedido.edite"],
    "gerente": ["pedidos.add", "pedidos.edite", "pedidos.delete"]
}

def converte_moeda(valor:int): 
    return f"{valor:,.2f}".replace(",", "-").replace(".", ",").replace("-", ".")



# dados da empresa
NOME     = "BOM SABOR ADS"
NIF      = "0002120"
TELEFONE = "931617941"
BANNER = "Bom sabores"

