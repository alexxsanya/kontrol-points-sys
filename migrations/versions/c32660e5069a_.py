"""empty message

Revision ID: c32660e5069a
Revises: 7de55ac55575
Create Date: 2019-04-30 13:36:06.932230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c32660e5069a'
down_revision = '7de55ac55575'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('kontrols', sa.Column('k_status', sa.String(length=25), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('kontrols', 'k_status')
    # ### end Alembic commands ###