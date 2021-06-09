"""empty message

Revision ID: a6e614b505b5
Revises: adf594338b91
Create Date: 2021-06-08 22:58:57.451404

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a6e614b505b5'
down_revision = 'adf594338b91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'sal',
               existing_type=mysql.VARCHAR(length=40),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'sal',
               existing_type=mysql.VARCHAR(length=40),
               nullable=False)
    # ### end Alembic commands ###
