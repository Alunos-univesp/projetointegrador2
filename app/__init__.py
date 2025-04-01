from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime  # Faltava importar isso!

# Instâncias globais
db = SQLAlchemy()
migrate = Migrate()

def create_app(testing=False):
    app = Flask(__name__)

    # 🔐 Chave secreta para sessões e flash
    app.secret_key = 'UNIVESP2025@controle'

    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Filtro personalizado para datas no Jinja
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%d-%m-%Y'):
        if value:
            try:
                return datetime.strptime(value, '%Y-%m-%d').strftime(format)
            except Exception:
                return value
        return 'Data não disponível'

    from app.routes import register_routes
    register_routes(app)

    return app
