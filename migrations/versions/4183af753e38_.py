"""empty message

Revision ID: 4183af753e38
Revises: 3d52176ea6f4
Create Date: 2015-05-11 18:33:35.187070

"""

# revision identifiers, used by Alembic.
revision = '4183af753e38'
down_revision = '3d52176ea6f4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('authenticated', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('email')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    ### end Alembic commands ###