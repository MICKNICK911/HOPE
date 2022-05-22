"""add few columns to posts table

Revision ID: c0e1a8d6d8af
Revises: 9d648f639758
Create Date: 2022-05-13 16:14:57.966973

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by ALEMBIC.
revision = 'c0e1a8d6d8af'
down_revision = '9d648f639758'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("created", sa.TIMESTAMP(timezone=True), nullable=False,
                                     server_default=sa.text("now()")))
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default='TRUE'))
    pass


def downgrade():
    op.drop_column("posts", 'created')
    op.drop_column("posts", 'published')
    pass
