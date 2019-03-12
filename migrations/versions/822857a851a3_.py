"""empty message

Revision ID: 822857a851a3
Revises: 
Create Date: 2019-03-12 08:29:46.187081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '822857a851a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kontrols',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('k_name', sa.String(length=128), nullable=False),
    sa.Column('k_utm', sa.Text(), nullable=False),
    sa.Column('k_created_by', sa.Text(), nullable=False),
    sa.Column('k_geocord', sa.String(length=250), nullable=True),
    sa.Column('k_addr_district', sa.String(length=250), nullable=False),
    sa.Column('k_addr_county', sa.String(length=250), nullable=True),
    sa.Column('k_addr_subcounty', sa.String(length=250), nullable=False),
    sa.Column('k_method_of_fixation', sa.Boolean(), nullable=True),
    sa.Column('k_equip_used', sa.String(length=100), nullable=False),
    sa.Column('k_surveyor', sa.String(length=100), nullable=False),
    sa.Column('k_descrition', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reviewed_by', sa.String(length=128), nullable=False),
    sa.Column('review_for', sa.String(length=128), nullable=False),
    sa.Column('kontrol_condition', sa.String(length=128), nullable=False),
    sa.Column('review_details', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.Column('u_firstname', sa.String(length=30), nullable=False),
    sa.Column('u_lastname', sa.String(length=30), nullable=False),
    sa.Column('u_telephone', sa.String(length=15), nullable=False),
    sa.Column('u_email', sa.String(length=35), nullable=False),
    sa.Column('u_district', sa.String(length=15), nullable=False),
    sa.Column('u_role', sa.String(length=15), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('u_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('reviews')
    op.drop_table('kontrols')
    # ### end Alembic commands ###
