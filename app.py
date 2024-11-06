from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import os
import sys
import logging
from sqlalchemy import func

# Configuração da aplicação Flask
app = Flask(__name__, template_folder='./templates')
app.secret_key = 'UNIVESP'

# Configuração do formato de data
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d-%m-%Y'):
    if value:
        return datetime.strptime(value, '%Y-%m-%d').strftime(format)
    return value

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://controle_estoque_postgres_user:wx35ZLHmY1gnRG62W6WPJqlqawQDDN8J@dpg-cslc0obv2p9s7383n3j0-a.oregon-postgres.render.com/controle_estoque_postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Inicializa o banco de dados SQLAlchemy e Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configuração do Firebase
def get_cred_file_path():
    application_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, 'controle-de-mercadoria-firebase-adminsdk-z1zlf-036e096d97.json')

cred_path = get_cred_file_path()
if os.path.isfile(cred_path):
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    firestore_db = firestore.client()
else:
    print("Firebase credential file not found.")

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
            return (data_validade_dt - datetime.now().date()).days
        return None

# Variável de controle para criação de tabelas
tables_created = False

@app.before_request
def create_tables():
    global tables_created
    if not tables_created:
        db.create_all()
        tables_created = True

# Rota principal e outras rotas de operação
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
    filtros = []
    for filtro, valor in {'nome': request.args.get('filtro_nome', ''), 'codigo': request.args.get('filtro_codigo', ''), 'marca': request.args.get('filtro_marca', '')}.items():
        if valor:
            filtros.append(getattr(Produto, filtro).like(f'%{valor}%'))
    produtos = Produto.query.filter(*filtros).all()
    return render_template('estoque.html', produtos=produtos)

@app.route('/excluir-produto/<int:id>', methods=['POST'])
def excluir_produto(id):
    produto = Produto.query.get(id)
    if produto:
        db.session.delete(produto)
        db.session.commit()
        return jsonify({'success': True}), 200
    return jsonify({'success': False}), 404

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

        # Firebase storage
        try:
            produto_ref = firestore_db.collection('produtos').document()
            produto_ref.set(dados_produto)
            flash('Produto cadastrado com sucesso no Firebase.', 'success')
        except Exception as e:
            app.logger.error(f"Erro ao salvar no Firestore: {e}")
            flash('Erro ao salvar no Firebase.', 'danger')

        return redirect(url_for('estoque'))
    return render_template('cadastro-mercadoria.html')

@app.route('/lista-produtos-proximo-vencimento')
def lista_produtos_proximo_vencimento():
    produtos = Produto.query.filter(
        (func.date(Produto.data_validade) - func.current_date()) <= 30
    ).all()
    return render_template('lista_produtos_proximo_vencimento.html', produtos=produtos)

@app.route('/detalhes-produto/<int:id>', methods=['GET'])
def detalhes_produto(id):
    produto = Produto.query.get(id)
    return jsonify({
        "id": produto.id,
        "nome": produto.nome,
        "categoria": produto.marca,
        "informacoes": produto.informacoes,
        "quantidade": produto.quantidade,
        "custo": produto.custo,
        "data_inclusao": produto.data_inclusao,
        "data_validade": produto.data_validade
    }) if produto else jsonify({"error": "Produto não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
