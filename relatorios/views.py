from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from openpyxl import Workbook

from transaccoes.models import Transaccao

class RelatorioVendasCompletoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Parâmetros
        start_date = request.query_params.get('start_date') or request.query_params.get('data_inicio')
        end_date = request.query_params.get('end_date') or request.query_params.get('data_fim')
        cliente_id = request.query_params.get('cliente_id') or request.query_params.get('cliente')
        produto_id = request.query_params.get('produto_id')
        tipo_pagamento = request.query_params.get('tipo_pagamento')
        tipo_transacao = request.query_params.get('tipo_transacao')

        transacoes = Transaccao.objects.all()

        if start_date:
            transacoes = transacoes.filter(data__date__gte=parse_date(start_date))
        if end_date:
            transacoes = transacoes.filter(data__date__lte=parse_date(end_date))
        if cliente_id:
            transacoes = transacoes.filter(cliente_id=cliente_id)
        if tipo_pagamento:
            transacoes = transacoes.filter(tipo_pagamento=tipo_pagamento)
        if tipo_transacao:
            transacoes = transacoes.filter(tipo=tipo_transacao)

        total_receita = 0
        total_produtos = 0
        vendas_por_produto = {}
        vendas_por_cliente = {}
        vendas_por_tipo_pagamento = {}
        ultimas_transacoes = []

        for t in transacoes:
            trans_total = 0
            for item in t.itens.all():
                preco_unit = item.produto.preco_venda if item.tipo == 'venda' else item.produto.preco_aluguer
                subtotal = preco_unit * item.quantidade
                trans_total += subtotal
                total_produtos += item.quantidade

                # Produto
                pid = item.produto.id
                if pid not in vendas_por_produto:
                    vendas_por_produto[pid] = {
                        'produto__id': pid,
                        'produto__nome': item.produto.nome,
                        'quantidade_vendida': 0,
                        'receita': 0,
                    }
                vendas_por_produto[pid]['quantidade_vendida'] += item.quantidade
                vendas_por_produto[pid]['receita'] += subtotal

            # Cliente
            cid = t.cliente.id
            if cid not in vendas_por_cliente:
                vendas_por_cliente[cid] = {
                    'cliente__id': cid,
                    'cliente__nome': t.cliente.nome,
                    'total_vendas': 0,
                    'num_transacoes': 0
                }
            vendas_por_cliente[cid]['total_vendas'] += trans_total
            vendas_por_cliente[cid]['num_transacoes'] += 1

            # Tipo pagamento
            tipo = t.tipo_pagamento
            if tipo not in vendas_por_tipo_pagamento:
                vendas_por_tipo_pagamento[tipo] = {
                    'tipo_pagamento': tipo,
                    'total': 0,
                    'num_transacoes': 0
                }
            vendas_por_tipo_pagamento[tipo]['total'] += trans_total
            vendas_por_tipo_pagamento[tipo]['num_transacoes'] += 1

            total_receita += trans_total

            # Últimas transações
            ultimas_transacoes.append({
                'id': t.id,
                'data': t.data,
                'cliente__nome': t.cliente.nome,
                'tipo_pagamento': t.tipo_pagamento,
            })

        return Response({
            'total_receita': total_receita,
            'total_transacoes': transacoes.count(),
            'total_produtos_vendidos': total_produtos,
            'vendas_por_produto': list(vendas_por_produto.values()),
            'vendas_por_cliente': list(vendas_por_cliente.values()),
            'vendas_por_tipo_pagamento': list(vendas_por_tipo_pagamento.values()),
            'ultimas_transacoes': sorted(ultimas_transacoes, key=lambda x: x['data'], reverse=True)[:10]
        })


def exportar_vendas_excel(request):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="vendas.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Vendas"

    ws.append(['ID Transação', 'Data', 'Cliente', 'Total'])

    transacoes = Transaccao.objects.all()
    for t in transacoes:
        total = 0
        for item in t.itens.all():
            preco_unit = item.produto.preco_venda if item.tipo == 'venda' else item.produto.preco_aluguer
            total += preco_unit * item.quantidade

        ws.append([t.id, t.data.strftime('%Y-%m-%d'), t.cliente.nome, total])

    wb.save(response)
    return response


def exportar_vendas_pdf(request):
    transacoes = Transaccao.objects.all()
    template = get_template('relatorios/vendas_pdf.html')  # Certifique-se do caminho
    html = template.render({'transacoes': transacoes})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="vendas.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF')

    return response
