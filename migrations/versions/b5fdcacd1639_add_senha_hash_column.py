"""Add senha_hash column

Revision ID: b5fdcacd1639
Revises: 843e87ced212
Create Date: 2024-04-28 22:49:21.163518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5fdcacd1639'
down_revision = '843e87ced212'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('senha_hash', sa.String(length=128), nullable=True))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=120),
               existing_nullable=True)
        batch_op.alter_column('nivel_acesso',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.drop_column('senha')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('senha', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.alter_column('nivel_acesso',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=10),
               existing_nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
        batch_op.drop_column('senha_hash')

    # ### end Alembic commands ###
