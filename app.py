from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import os
import sys
import logging

# Configuração da aplicação Flask
app = Flask(__name__, template_folder='./templates')
app.secret_key = 'UNIVESP'

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d-%m-%Y'):
    if value:
        return datetime.strptime(value, '%Y-%m-%d').strftime(format)
    return value

# Configuração da URI do MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/controle_estoque'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados SQLAlchemy e Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configuração do Firebase
def get_cred_file_path():
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    cred_file_name = 'controle-de-mercadoria-firebase-adminsdk-z1zlf-036e096d97.json'
    return os.path.join(application_path, cred_file_name)

cred_path = get_cred_file_path()
print(f"Path to credential file: {cred_path}")

if os.path.isfile(cred_path):
    print("File exists.")
else:
    print("File does not exist.")

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()

# Definição dos modelos de banco de dados
class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.Float, default=0.0)
    custo = db.Column(db.Float)
    marca = db.Column(db.String(100))  # Usado para armazenar a categoria
    informacoes = db.Column(db.Text)
    quantidade = db.Column(db.Integer)
    data_inclusao = db.Column(db.String(100))
    data_validade = db.Column(db.String(100))

    @property
    def dias_ate_vencimento(self):
        if self.data_validade:
            data_validade_dt = datetime.strptime(self.data_validade, '%Y-%m-%d').date()
            hoje = datetime.now().date()
            dias_ate_vencimento = (data_validade_dt - hoje).days
            return dias_ate_vencimento
        return None

# Variável de controle para criação de tabelas
tables_created = False

@app.before_request
def create_tables():
    global tables_created
    if not tables_created:
        db.create_all()
        tables_created = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/estoque', methods=['GET', 'POST'])
def estoque():
    filtro_nome = request.args.get('filtro_nome', '')
    filtro_codigo = request.args.get('filtro_codigo', '')
    filtro_marca = request.args.get('filtro_marca', '')

    filtros = []
    if filtro_nome:
        filtros.append(Produto.nome.like(f'%{filtro_nome}%'))
    if filtro_codigo:
        filtros.append(Produto.codigo.like(f'%{filtro_codigo}%'))
    if filtro_marca:
        filtros.append(Produto.marca.like(f'%{filtro_marca}%'))

    produtos = Produto.query.filter(*filtros).all()
    return render_template('estoque.html', produtos=produtos)

@app.route('/excluir-produto/<int:id>', methods=['POST'])
def excluir_produto(id):
    produto = Produto.query.get(id)
    if produto:
        db.session.delete(produto)
        db.session.commit()
        flash('Produto excluído com sucesso.', 'success')
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 404

@app.route('/cadastro-mercadoria', methods=['GET', 'POST'])
def cadastro_mercadoria():
    if request.method == 'POST':
        nome_produto = request.form.get('nomeProduto')
        categoria_produto = request.form.get('categoria')  # Corrigido para categoria
        informacoes_produto = request.form.get('informacoesProduto')
        codigo = request.form.get('codigo')
        custo = request.form.get('custo')
        quantidade = request.form.get('quantidadeProduto')
        data_cadastro = request.form.get('dataCadastro')
        data_validade = request.form.get('dataValidade')

        novo_produto = Produto(
            nome=nome_produto,
            marca=categoria_produto,  # Armazena a categoria em 'marca'
            informacoes=informacoes_produto,
            custo=custo,
            quantidade=quantidade,
            data_inclusao=data_cadastro,
            data_validade=data_validade,
            codigo=codigo
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso.', 'success')

        try:
            produto_ref = firestore_db.collection('produtos').document()
            produto_ref.set({
                'nome': nome_produto,
                'categoria': categoria_produto,
                'informacoes': informacoes_produto,
                'codigo': codigo,
                'custo': custo,
                'quantidade': quantidade,
                'data_inclusao': data_cadastro,
                'data_validade': data_validade
            })
            flash('Produto cadastrado com sucesso no Firebase.', 'success')
        except Exception as e:
            app.logger.error(f"Erro ao salvar no Firestore: {e}")
            flash('Erro ao salvar no Firebase.', 'danger')

        return redirect(url_for('estoque'))
    return render_template('cadastro-mercadoria.html')

@app.route('/lista-produtos-proximo-vencimento')
def lista_produtos_proximo_vencimento():
    produtos = Produto.query.filter(
        db.func.DATEDIFF(Produto.data_validade, db.func.now()) <= 30
    ).all()
    return render_template('lista_produtos_proximo_vencimento.html', produtos=produtos)

@app.route('/detalhes-produto/<int:id>', methods=['GET'])
def detalhes_produto(id):
    produto = Produto.query.get(id)
    if produto:
        detalhes = {
            "id": produto.id,
            "nome": produto.nome,
            "categoria": produto.marca,  # Ajustado para mostrar a categoria
            "informacoes": produto.informacoes,
            "quantidade": produto.quantidade,
            "custo": produto.custo,
            "data_inclusao": produto.data_inclusao,
            "data_validade": produto.data_validade
        }
        return jsonify(detalhes), 200
    else:
        return jsonify({"error": "Produto não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)