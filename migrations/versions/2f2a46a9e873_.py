"""empty message

Revision ID: 2f2a46a9e873
Revises: 
Create Date: 2022-08-19 00:56:27.015636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f2a46a9e873'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('groupID', sa.Integer(), nullable=False),
    sa.Column('store', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('groupID')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('nickname', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id', 'nickname')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('group')
    # ### end Alembic commands ###
