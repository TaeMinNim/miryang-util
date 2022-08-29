"""empty message

Revision ID: 36b405cbc8c2
Revises: 2f2a46a9e873
Create Date: 2022-08-19 14:53:51.385413

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36b405cbc8c2'
down_revision = '2f2a46a9e873'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('id', sa.INTEGER(), nullable=False))
    # ### end Alembic commands ###