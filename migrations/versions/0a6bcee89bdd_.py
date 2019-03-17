"""empty message

Revision ID: 0a6bcee89bdd
Revises: 
Create Date: 2019-03-18 01:23:03.494644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a6bcee89bdd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.Column('u_firstname', sa.String(length=30), nullable=False),
    sa.Column('u_lastname', sa.String(length=30), nullable=False),
    sa.Column('u_telephone', sa.String(length=15), nullable=False),
    sa.Column('u_email', sa.String(length=35), nullable=False),
    sa.Column('u_password', sa.String(length=150), nullable=False),
    sa.Column('u_role', sa.String(length=15), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('u_id'),
    sa.UniqueConstraint('u_email'),
    sa.UniqueConstraint('u_telephone')
    )
    op.create_table('kontrols',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('k_name', sa.String(length=50), nullable=False),
    sa.Column('k_utm', sa.String(length=50), nullable=False),
    sa.Column('k_geocord', sa.String(length=50), nullable=True),
    sa.Column('k_addr_district', sa.String(length=25), nullable=False),
    sa.Column('k_addr_county', sa.String(length=50), nullable=True),
    sa.Column('k_addr_subcounty', sa.String(length=50), nullable=False),
    sa.Column('k_method_of_fixation', sa.String(length=50), nullable=True),
    sa.Column('k_equip_used', sa.String(length=50), nullable=False),
    sa.Column('k_surveyor', sa.String(length=50), nullable=True),
    sa.Column('k_description', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.u_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('k_geocord'),
    sa.UniqueConstraint('k_name')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kontrol_condition', sa.String(length=50), nullable=False),
    sa.Column('review_details', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('kontrol_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['kontrol_id'], ['kontrols.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.u_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    op.drop_table('kontrols')
    op.drop_table('users')
    # ### end Alembic commands ###
