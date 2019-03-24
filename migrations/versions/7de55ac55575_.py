"""empty message

Revision ID: 7de55ac55575
Revises: 0a6bcee89bdd
Create Date: 2019-03-25 02:28:30.353984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7de55ac55575'
down_revision = '0a6bcee89bdd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('kontrol_foto', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reviews', 'kontrol_foto')
    # ### end Alembic commands ###
