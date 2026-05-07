import csv
from io import StringIO, BytesIO
from datetime import datetime, time

from flask import redirect, url_for
from flask_login import current_user
from flask import request, send_file
from flask_admin import expose, BaseView

from .base import Model
from utils import converte_moeda
from models import Pedido, ItenPedido, Usuario


def parse_date(value):
    """
    Aceita:
    - 2025-01-31
    - 31-01-2025
    - 31/01/2025
    """
    if not value:
        return None

    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    return None

class PedidoType:
    def __init__(self, query:Pedido):
        self.numero = query.id
        self.produtos = query.produtos.select().count()
        self.total = converte_moeda( query.total)
        self.data = query.fechado_em.strftime("%d/%m/%Y %H:%M")
    

class RelatoriosAdmin(BaseView):
    
    roles = ["admin", "gestor"]
    user = None
    
    def set_roles(self):
        ...
    
    def is_accessible(self):
                
        view = False
        self.user:Usuario = current_user
        if self.user.is_authenticated and self.user.user_type in self.roles:
            view = True
            self.set_roles()
        return view

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))

    def _get_query_filtrada(self):
        start = request.args.get("inicio", "").strip()
        end   = request.args.get("fim", "").strip()

        query = Pedido.select().where(Pedido.status == Pedido.Status.finalizado)

        
        # data inicial
        data_inicio = parse_date(start)
        if data_inicio:
            query = query.where(Pedido.fechado_em >= data_inicio)

        # data final (até 23:59:59)
        data_fim = parse_date(end)
        if data_fim:
            data_fim = datetime.combine(data_fim.date(), time.max)
            query = query.where(Pedido.fechado_em <= data_fim)
        return (query, (start, end))

    def _get_resumo(self, query:Pedido):
        
        lst_pedidos = [ float(p.total) for p in query]
        
        class obj:
            produtos = sum( [ i.produtos.select().count() for i in query] )
            pedidos  = query.count()
            vendas   = sum(lst_pedidos)
            try:
                media    = converte_moeda(vendas / pedidos)
            except:
                media = converte_moeda(0)
            vendas = converte_moeda(vendas)
            
            
        return obj
    
    def _export_csv(self, query:Pedido):
        output = StringIO()
        writer = csv.writer(output)

        # cabeçalho
        writer.writerow([
            "Pedido",
            "Produtos",
            "Total",
            "Data/hora",
        ])

        for p in query:
            writer.writerow([
                p.id,
                p.produtos.select().count(),
                converte_moeda(p.total),
                p.fechado_em.strftime("%d/%m/%Y %H:%M")
            ])

        mem = BytesIO()
        mem.write(output.getvalue().encode("utf-8"))
        mem.seek(0)

        filename = f"relatorio_pedidos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        return send_file(
            mem,
            mimetype="text/csv",
            as_attachment=True,
            download_name=filename
        )
    
    @expose("/", methods=["GET", "POST"])
    def index(self):
        
        query, infos_data = self._get_query_filtrada()
        
        # 👉 Se tiver export, gera CSV
        if request.args.get("export"):
            return self._export_csv(query)
        
        class dados:
            resumo = self._get_resumo(query)

            lista_pedidos = (
                PedidoType(p)
                for p in query
            )
            
        return self.render("admin/relatorio.html", dados=dados)

    
    
    
   