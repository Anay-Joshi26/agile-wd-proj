"""added a game performance db model, and updated the Game db model to hold a creation date and upvotes counter

Revision ID: e3c4d81b82d8
Revises: c4fda3b81da3
Create Date: 2024-05-06 21:10:36.702038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3c4d81b82d8'
down_revision = 'c4fda3b81da3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game_performance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('attempts', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.gameId'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('number_of_upvotes', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('date_created', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_column('date_created')
        batch_op.drop_column('number_of_upvotes')

    op.drop_table('game_performance')
    # ### end Alembic commands ###
