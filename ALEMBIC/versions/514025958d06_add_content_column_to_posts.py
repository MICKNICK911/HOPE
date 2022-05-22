"""add_content_column_to_posts

Revision ID: 514025958d06
Revises: d5d13518e885
Create Date: 2022-05-13 09:33:33.578249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by ALEMBIC.
revision = '514025958d06'
down_revision = 'd5d13518e885'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", 'content')
    pass
