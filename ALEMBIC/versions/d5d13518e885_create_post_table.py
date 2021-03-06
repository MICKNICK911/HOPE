"""create post table

Revision ID: d5d13518e885
Revises: 
Create Date: 2022-05-13 08:28:12.070719

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by ALEMBIC.
revision = 'd5d13518e885'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
