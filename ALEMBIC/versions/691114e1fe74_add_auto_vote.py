"""add auto vote

Revision ID: 691114e1fe74
Revises: c0e1a8d6d8af
Create Date: 2022-05-13 16:49:43.415261

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by ALEMBIC.
revision = '691114e1fe74'
down_revision = 'c0e1a8d6d8af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by ALEMBIC - please adjust! ###
    op.create_table('vote',
                    sa.Column('post_ids', sa.Integer(), nullable=False),
                    sa.Column('user_ids', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_ids'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_ids'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('post_ids', 'user_ids')
                    )
    # ### end ALEMBIC commands ###


def downgrade():
    # ### commands auto generated by ALEMBIC - please adjust! ###
    op.drop_table('vote')
    # ### end ALEMBIC commands ###
