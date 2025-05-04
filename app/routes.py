from flask import render_template, request, redirect, url_for, flash, jsonify, send_file
from app.models import Produto
from app import db
from sqlalchemy import func
from io import BytesIO
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from markupsafe import Markup
import pdfkit
import base64
from datetime import datetime

def register_routes(app):

    # ⚠️ Cria tabelas em cada request — use apenas em desenvolvimento
    @app.before_request
    def create_tables():
        db.create_all()

    # 🔐 Tela de login (Firebase)
    @app.route('/')
    def index():
        return render_template('index.html')

    # 🔁 Rota adicional para evitar erro 404 ao acessar /login
    @app.route('/login')
    def login():
        return redirect('/')

    # 🏠 Tela inicial após login
    @app.route('/home')
    def home():
        return render_template('home.html')

    # 📦 Visualização do estoque com filtros
    @app.route('/estoque')
    def estoque():
        filtros = []
        for filtro, valor in {
            'nome': request.args.get('filtro_nome', ''),
            'codigo': request.args.get('filtro_codigo', ''),
            'marca': request.args.get('filtro_marca', '')
        }.items():
            if valor:
                filtros.append(getattr(Produto, filtro).like(f"%{valor}%"))
        produtos = Produto.query.filter(*filtros).all()
        return render_template('estoque.html', produtos=produtos)

    # ➕ Cadastro de mercadoria
    @app.route('/cadastro-mercadoria', methods=['GET', 'POST'])
    def cadastro_mercadoria():
        if request.method == 'POST':
            dados_produto = {
                'nome': request.form.get('nomeProduto'),
                'marca': request.form.get('categoria'),
                'informacoes': request.form.get('informacoesProduto'),
                'codigo': request.form.get('codigo'),
                'custo': request.form.get('custo'),
                'quantidade': request.form.get('quantidadeProduto'),
                'data_inclusao': request.form.get('dataCadastro'),
                'data_validade': request.form.get('dataValidade')
            }
            novo_produto = Produto(**dados_produto)
            db.session.add(novo_produto)
            db.session.commit()
            flash('Produto cadastrado com sucesso.', 'success')
            return redirect(url_for('estoque'))
        return render_template('cadastro-mercadoria.html')

    # ❌ Excluir produto
    @app.route('/excluir-produto/<int:id>', methods=['POST'])
    def excluir_produto(id):
        produto = Produto.query.get(id)
        if produto:
            db.session.delete(produto)
            db.session.commit()
            return jsonify({'success': True}), 200
        return jsonify({'success': False}), 404

    # ⏳ Lista produtos que vencem em até 30 dias
    @app.route('/lista-produtos-proximo-vencimento')
    def lista_produtos_proximo_vencimento():
        produtos = Produto.query.all()
        proximos = [p for p in produtos if p.dias_ate_vencimento is not None and p.dias_ate_vencimento <= 30]
        return render_template('lista_produtos_proximo_vencimento.html', produtos=proximos)

    # 🔗 API pública com dados dos produtos
    @app.route('/api/produtos', methods=['GET'])
    def api_listar_produtos():
        produtos = Produto.query.all()
        return jsonify([{
            "id": p.id,
            "nome": p.nome,
            "quantidade": p.quantidade,
            "data_validade": p.data_validade
        } for p in produtos])

    # 📡 Simulação de sensor IoT
    @app.route('/iot/sensor')
    def sensor_simulado():
        return jsonify({"temperatura": 22.5, "umidade": 60})

    # 📁 Download do estoque em Excel
    @app.route('/download_excel')
    def download_excel():
        produtos = Produto.query.all()
        data = {
            "ID": [p.id for p in produtos],
            "Nome": [p.nome for p in produtos],
            "Código": [p.codigo for p in produtos],
            "Marca": [p.marca for p in produtos],
            "Informações": [p.informacoes for p in produtos],
            "Quantidade": [p.quantidade for p in produtos],
            "Custo": [p.custo for p in produtos],
            "Data de Inclusão": [p.data_inclusao for p in produtos],
            "Data de Validade": [p.data_validade for p in produtos],
            "Dias até Vencimento": [p.dias_ate_vencimento for p in produtos]
        }
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Estoque')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='estoque_produtos.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # 📊 Visualização dos gráficos (estoque, categorias, vencidos)
    @app.route('/analise')
    def analise():
        produtos = Produto.query.all()

        nomes = [p.nome for p in produtos]
        quantidades = [p.quantidade for p in produtos]
        fig_estoque = go.Figure([go.Bar(x=nomes, y=quantidades)])
        fig_estoque.update_layout(title='Quantidade em Estoque por Produto', xaxis_title='Produto', yaxis_title='Quantidade')
        grafico_estoque = pio.to_html(fig_estoque, full_html=False)

        categorias = {}
        for p in produtos:
            if p.marca:
                categorias[p.marca] = categorias.get(p.marca, 0) + p.quantidade
        fig_categoria = go.Figure([go.Pie(labels=list(categorias.keys()), values=list(categorias.values()))])
        fig_categoria.update_layout(title='Distribuição de Estoque por Categoria')
        grafico_categoria = pio.to_html(fig_categoria, full_html=False)

        vencidos = {}
        for p in produtos:
            if p.data_validade:
                try:
                    if datetime.strptime(p.data_validade, '%Y-%m-%d').date() < datetime.now().date():
                        vencidos[p.nome] = p.quantidade
                except:
                    continue
        fig_vencidos = go.Figure([go.Bar(x=list(vencidos.keys()), y=list(vencidos.values()))])
        fig_vencidos.update_layout(title='Produtos Vencidos', xaxis_title='Produto', yaxis_title='Quantidade')
        grafico_vencidos = pio.to_html(fig_vencidos, full_html=False)

        return render_template('analise.html',
            grafico_estoque=Markup(grafico_estoque),
            grafico_categoria=Markup(grafico_categoria),
            grafico_vencidos=Markup(grafico_vencidos)
        )

    # 🧾 Geração de relatório em PDF com gráfico
    @app.route('/analise/pdf')
    def gerar_pdf():
        produtos = Produto.query.all()
        nomes = [p.nome for p in produtos]
        quantidades = [p.quantidade for p in produtos]

        fig = go.Figure([go.Bar(x=nomes, y=quantidades)])
        fig.update_layout(title='Estoque de Produtos', xaxis_title='Produto', yaxis_title='Quantidade')
        img_bytes = fig.to_image(format="png")
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        html = render_template("pdf_analise.html", grafico=img_base64)
        pdf = pdfkit.from_string(html, False, configuration=config)

        return send_file(BytesIO(pdf), download_name="relatorio_estoque.pdf", as_attachment=True)
