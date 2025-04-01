from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=1, max=100)])
    validade = DateField('Validade', validators=[DataRequired()], format='%Y-%m-%d')
    categoria = StringField('Categoria', validators=[DataRequired(), Length(min=1, max=50)])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=0)])
    preco = DecimalField('Preço', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Salvar')
