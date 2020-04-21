"""empty message

Revision ID: 1957db135c8b
Revises: ec5f1f66d42a
Create Date: 2020-04-20 12:51:58.014085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1957db135c8b'
down_revision = 'ec5f1f66d42a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('ads_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ads_id'], ['ads.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_ads_id'), 'comment', ['ads_id'], unique=False)
    op.create_index(op.f('ix_comment_user_id'), 'comment', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comment_user_id'), table_name='comment')
    op.drop_index(op.f('ix_comment_ads_id'), table_name='comment')
    op.drop_table('comment')
    # ### end Alembic commands ###