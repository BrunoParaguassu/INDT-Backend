"""primeiro teste de  migração

Revision ID: 843e87ced212
Revises: 
Create Date: 2024-04-28 11:38:22.384936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '843e87ced212'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.Column('sobrenome', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('senha', sa.String(length=100), nullable=True),
    sa.Column('nivel_acesso', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
