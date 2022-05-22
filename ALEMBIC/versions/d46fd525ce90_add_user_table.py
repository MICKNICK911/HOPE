"""add user table

Revision ID: d46fd525ce90
Revises: 514025958d06
Create Date: 2022-05-13 11:16:27.908796

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd46fd525ce90'
down_revision = '514025958d06'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created", sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table("users")
    pass
