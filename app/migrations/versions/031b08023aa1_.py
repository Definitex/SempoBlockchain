"""Custom attribute indexes

Revision ID: 031b08023aa1
Revises: 6488be258421
Create Date: 2020-11-18 15:56:53.861776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '031b08023aa1'
down_revision = '6488be258421'
branch_labels = None
depends_on = None


def upgrade():
    return True
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_custom_attribute_id'), 'custom_attribute', ['id'], unique=False)
    op.create_index(op.f('ix_custom_attribute_name'), 'custom_attribute', ['name'], unique=False)
    op.create_index(op.f('ix_custom_attribute_user_storage_id'), 'custom_attribute_user_storage', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    return True
    op.drop_index(op.f('ix_custom_attribute_user_storage_id'), table_name='custom_attribute_user_storage')
    op.drop_index(op.f('ix_custom_attribute_name'), table_name='custom_attribute')
    op.drop_index(op.f('ix_custom_attribute_id'), table_name='custom_attribute')
    # ### end Alembic commands ###
