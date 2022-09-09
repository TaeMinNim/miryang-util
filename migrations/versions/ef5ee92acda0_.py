"""empty message

Revision ID: ef5ee92acda0
Revises: e2b9cc9d4d1f
Create Date: 2022-08-31 14:09:29.197305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef5ee92acda0'
down_revision = 'e2b9cc9d4d1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'USER', type_='foreignkey')
    op.create_foreign_key(None, 'USER', 'ORDER_GROUP', ['joinGroup'], ['groupID'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'USER', type_='foreignkey')
    op.create_foreign_key(None, 'USER', 'ORDER_GROUP', ['joinGroup'], ['groupID'], ondelete='CASCADE')
    # ### end Alembic commands ###
