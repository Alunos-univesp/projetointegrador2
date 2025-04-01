import pytest
from app import create_app, db
from app.models import Produto

@pytest.fixture
def client():
    app = create_app(testing=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_home_page(client):
    response = client.get('/home')
    assert response.status_code == 200

def test_estoque_page(client):
    response = client.get('/estoque')
    assert response.status_code in [200, 302]

def test_api_produtos(client):
    response = client.get('/api/produtos')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_sensor_simulado(client):
    response = client.get('/iot/sensor')
    assert response.status_code == 200
    assert 'temperatura' in response.json
    assert 'umidade' in response.json

def test_cadastro_produto(client):
    data = {
        'nomeProduto': 'Produto Teste',
        'categoria': 'Categoria Teste',
        'informacoesProduto': 'Teste via formulário',
        'codigo': '123456',
        'custo': '12.50',
        'quantidadeProduto': '5',
        'dataCadastro': '2025-03-31',
        'dataValidade': '2025-12-31'
    }
    response = client.post('/cadastro-mercadoria', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Produto cadastrado com sucesso' in response.data

def test_download_excel(client):
    response = client.get('/download_excel')
    assert response.status_code == 200
    assert response.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

def test_analise_estoque(client):
    response = client.get('/analise')
    assert response.status_code == 200
    assert b'Estoque' in response.data or b'Gr\xc3\xa1fico' in response.data
