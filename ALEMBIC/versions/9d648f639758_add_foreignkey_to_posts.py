"""add foreignkey to posts

Revision ID: 9d648f639758
Revises: d46fd525ce90
Create Date: 2022-05-13 12:19:26.079520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by ALEMBIC.
revision = '9d648f639758'
down_revision = 'd46fd525ce90'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['user_id'],
                          remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
