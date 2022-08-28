"""empty message

Revision ID: 07ccec49bae8
Revises: 61b2da97fe66
Create Date: 2022-08-26 12:04:26.727415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07ccec49bae8'
down_revision = '61b2da97fe66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('time', sa.DateTime(), nullable=True))
    op.add_column('group', sa.Column('delivery_cost', sa.Integer(), nullable=True))
    op.add_column('group', sa.Column('account_number', sa.String(length=50), nullable=True))
    op.add_column('group', sa.Column('repUserId', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'group', 'user', ['repUserId'], ['id'])
    op.add_column('user', sa.Column('joinGroup', sa.Integer(), nullable=True))
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.create_unique_constraint(None, 'user', ['nickname'])
    op.create_foreign_key(None, 'user', 'group', ['joinGroup'], ['groupID'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='unique')
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.drop_column('user', 'joinGroup')
    op.drop_constraint(None, 'group', type_='foreignkey')
    op.drop_column('group', 'repUserId')
    op.drop_column('group', 'account_number')
    op.drop_column('group', 'delivery_cost')
    op.drop_column('group', 'time')
    # ### end Alembic commands ###
