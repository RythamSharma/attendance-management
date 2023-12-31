"""empty message

Revision ID: 8a6e4f7d10bb
Revises: f9683df0924a
Create Date: 2023-04-09 03:26:20.407505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a6e4f7d10bb'
down_revision = 'f9683df0924a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rollto_name',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('roll_number', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rollto_name')
    # ### end Alembic commands ###
