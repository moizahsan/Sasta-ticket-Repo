"""empty message

Revision ID: 481f26927dfc
Revises: e70bfc237745
Create Date: 2022-05-12 13:11:54.783296

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '481f26927dfc'
down_revision = 'e70bfc237745'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quote', sa.Column('param', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quote', 'param')
    # ### end Alembic commands ###
