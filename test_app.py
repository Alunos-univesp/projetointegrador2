import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # banco em memória temporário
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_home_page(client):
    response = client.get('/home')
    assert response.status_code == 200

def test_estoque_page(client):
    response = client.get('/estoque')
    assert response.status_code in [200, 302]  # pode redirecionar se exigir login
