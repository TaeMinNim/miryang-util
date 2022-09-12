"""empty message

Revision ID: 2006facba0cd
Revises: 59ea5e8d8658
Create Date: 2022-09-12 11:52:27.747381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2006facba0cd'
down_revision = '59ea5e8d8658'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('GROUP',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('repUserId', sa.Integer(), nullable=True),
    sa.Column('joinuser', sa.Integer(), nullable=True),
    sa.Column('store', sa.String(length=50), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('delivery_cost', sa.Integer(), nullable=True),
    sa.Column('account_number', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['repUserId'], ['USER.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('USER',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('nickname', sa.String(length=20), nullable=False),
    sa.Column('userID', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('joinGroup', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['joinGroup'], ['GROUP.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nickname'),
    sa.UniqueConstraint('userID')
    )
    op.create_table('ORDER',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('groupID', sa.Integer(), nullable=True),
    sa.Column('userID', sa.Integer(), nullable=True),
    sa.Column('menu', sa.String(length=50), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('option', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['groupID'], ['GROUP.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['userID'], ['USER.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ORDER')
    op.drop_table('USER')
    op.drop_table('GROUP')
    # ### end Alembic commands ###
