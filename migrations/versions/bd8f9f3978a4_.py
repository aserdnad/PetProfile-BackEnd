"""empty message

Revision ID: bd8f9f3978a4
Revises: e22084dc913d
Create Date: 2021-06-19 08:10:53.144944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd8f9f3978a4'
down_revision = 'e22084dc913d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photo_add', sa.Column('token_image', sa.String(length=150), nullable=False))
    op.create_unique_constraint(None, 'photo_add', ['token_image'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'photo_add', type_='unique')
    op.drop_column('photo_add', 'token_image')
    # ### end Alembic commands ###
