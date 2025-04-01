from . import db
from datetime import datetime

class Produto(db.Model):
    __tablename__ = 'produtos'
    __table_args__ = {'extend_existing': True}  # ← Solução do problema

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
            data_validade_dt = datetime.strptime(self.data_validade, '%Y-%m-%d').date()
            return (data_validade_dt - datetime.now().date()).days
        return None
