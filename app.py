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
# Filtro personalizado para formatar datas
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d-%m-%Y'):
    if value:
        return datetime.strptime(value, '%Y-%m-%d').strftime(format)
    return value
app.secret_key = 'UNIVESP'

# Configuração da URI do MySQL - Substitua com suas credenciais reais
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/controle_estoque'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados SQLAlchemy
db = SQLAlchemy(app)

# Inicializa o Flask-Migrate
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
    marca = db.Column(db.String(100))
    informacoes = db.Column(db.Text)
    quantidade = db.Column(db.Integer)
    data_inclusao = db.Column(db.String(100))
    data_validade = db.Column(db.String(100))

    @property
    def dias_ate_vencimento(self):
        if self.data_validade:
            data_validade_dt = datetime.strptime(self.data_validade, '%Y-%m-%d')
            hoje = datetime.now()
            dias_ate_vencimento = (data_validade_dt - hoje).days
            return dias_ate_vencimento
        return None

class Saida(db.Model):
    __tablename__ = 'saidas'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_saida = db.Column(db.String(100), nullable=False)

# Inicializa o banco de dados, criando as tabelas
@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    app.logger.debug('Rendering index.html')
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/estoque', methods=['GET', 'POST'])
def estoque():
    # Definir os filtros com valores padrão vazios
    filtro_nome = request.form.get('filtro_nome', '') if request.method == 'POST' else request.args.get('filtro_nome', '')
    filtro_codigo = request.form.get('filtro_codigo', '') if request.method == 'POST' else request.args.get('filtro_codigo', '')
    filtro_marca = request.form.get('filtro_marca', '') if request.method == 'POST' else request.args.get('filtro_marca', '')

    # Criar uma lista de condições dinâmicas
    filtros = []
    if filtro_nome:
        filtros.append(Produto.nome.like(f'%{filtro_nome}%'))
    if filtro_codigo:
        filtros.append(Produto.codigo.like(f'%{filtro_codigo}%'))
    if filtro_marca:
        filtros.append(Produto.marca.like(f'%{filtro_marca}%'))

    # Aplicar os filtros no banco de dados
    produtos = Produto.query.filter(*filtros).all()

    return render_template('estoque.html', produtos=produtos)

@app.route('/excluir-produto/<int:id>', methods=['POST'])
def excluir_produto(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('estoque'))

@app.route('/editar-produto/<int:produto_id>', methods=['POST'])
def editar_produto(produto_id):
    try:
        app.logger.info(f'Recebendo solicitação para editar o produto com ID: {produto_id}')
        produto = Produto.query.get(produto_id)
        if not produto:
            return jsonify({"success": False, "error": "Produto não encontrado."}), 404

        # Pegando os dados enviados
        nome = request.form.get('nome')
        marca = request.form.get('marca')
        informacoes = request.form.get('informacoes')
        codigo = request.form.get('codigo')
        custo = request.form.get('custo')
        quantidade = request.form.get('quantidade')
        data_inclusao = request.form.get('data_inclusao')
        data_validade = request.form.get('data_validade')

        # Verificar no log se os dados estão corretos
        app.logger.info(f"Data de validade recebida: {data_validade}")

        if not all([nome, marca, codigo, custo, quantidade, data_inclusao, data_validade]):
            return jsonify({"success": False, "error": "Todos os campos são obrigatórios."}), 400

        # Atualizar os campos do produto
        produto.nome = nome
        produto.marca = marca
        produto.informacoes = informacoes
        produto.codigo = float(codigo)
        produto.custo = float(custo)
        produto.quantidade = int(quantidade)
        produto.data_inclusao = data_inclusao
        produto.data_validade = data_validade

        db.session.commit()

        # Atualizar o Firestore (caso esteja usando)
        produto_ref = firestore_db.collection('produtos').document(str(produto_id))
        produto_ref.update({
            'nome': produto.nome,
            'marca': produto.marca,
            'informacoes': produto.informacoes,
            'codigo': float(produto.codigo),
            'custo': float(produto.custo),
            'quantidade': int(produto.quantidade),
            'data_inclusao': produto.data_inclusao,
            'data_validade': produto.data_validade
        })

        return jsonify({"success": True})
    except Exception as e:
        app.logger.error(f"Erro ao atualizar o produto: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/cadastro-mercadoria', methods=['GET', 'POST'])
def cadastro_mercadoria():
    if request.method == 'POST':
        nome_produto = request.form.get('nomeProduto')
        marca_produto = request.form.get('marcaProduto')
        informacoes_produto = request.form.get('informacoesProduto')
        codigo = str(request.form.get('codigo'))
        custo = request.form.get('custo')
        quantidade = request.form.get('quantidadeProduto')
        data_cadastro = request.form.get('dataCadastro')
        data_validade = request.form.get('dataValidade')

        novo_produto = Produto(
            nome=nome_produto,
            marca=marca_produto,
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
                'marca': marca_produto,
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

@app.route('/processar-venda', methods=['POST'])
def processar_venda():
    produto_id = request.form.get('produto_id')
    quantidade_vendida = int(request.form.get('quantidade'))
    produto = Produto.query.get(produto_id)
    
    if produto and produto.quantidade >= quantidade_vendida:
        produto.quantidade -= quantidade_vendida
        db.session.commit()
        flash('Venda processada com sucesso!', 'success')
    else:
        flash('Erro: Quantidade insuficiente em estoque.', 'danger')

    return redirect(url_for('estoque'))

@app.route('/registrar_saida', methods=['POST'])
def registrar_saida():
    produto_id = request.form.get('produto_id')
    quantidade = int(request.form.get('quantidade'))
    produto = Produto.query.get(produto_id)
    
    if produto and produto.quantidade >= quantidade:
        produto.quantidade -= quantidade
        db.session.commit()
        nova_saida = Saida(
            produto_id=produto_id,
            quantidade=quantidade,
            data_saida=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(nova_saida)
        db.session.commit()
        flash('Saída de produto registrada com sucesso!', 'success')
    else:
        flash('Erro: Produto não encontrado ou quantidade insuficiente.', 'danger')

    return redirect(url_for('estoque'))

if __name__ == '__main__':
    app.run(debug=True)