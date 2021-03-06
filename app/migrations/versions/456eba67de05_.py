"""empty message

Adding blockchain_task_uuid index to worker messages

Revision ID: 456eba67de05
Revises: 380a71c24bba
Create Date: 2020-11-17 16:10:54.184490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '456eba67de05'
down_revision = '380a71c24bba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_worker_messages_blockchain_task_uuid'), 'worker_messages', ['blockchain_task_uuid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_worker_messages_blockchain_task_uuid'), table_name='worker_messages')
    # ### end Alembic commands ###
