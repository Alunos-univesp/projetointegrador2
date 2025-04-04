"""Descrição da nova migração

Revision ID: d5f22ddb33de
Revises: 
Create Date: 2024-11-05 21:37:15.080669

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd5f22ddb33de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('saidas')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('saidas',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('produto_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantidade', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('data_saida', mysql.VARCHAR(length=100), nullable=False),
    sa.ForeignKeyConstraint(['produto_id'], ['produtos.id'], name='saidas_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
