from .base import Model

class PagamentoAdmin(Model):
    column_list = ["assinatura", "entidade", "referencia", "valor", "status", "expira_em"]



