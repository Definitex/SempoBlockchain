"""adds chain name to token

Revision ID: 04be49fe82d4
Revises: 9a0d2407d3ed
Create Date: 2020-10-14 14:03:25.776682

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


# revision identifiers, used by Alembic.
revision = '04be49fe82d4'
down_revision = '9a0d2407d3ed'
branch_labels = None
depends_on = None

Base = declarative_base()

class Token(Base):
    __tablename__ = 'token'
    id = sa.Column(sa.Integer, primary_key=True)
    chain = sa.Column(sa.String)

def upgrade():
    conn = op.get_bind()
    session = Session(bind=conn)

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('token', sa.Column('chain', sa.String(), default='ETHEREUM', nullable=True))
    for o in session.query(Token).execution_options(show_all=True).all():
        if not o.chain:
            o.chain = 'ETHEREUM'
    session.commit()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('token', 'chain')
    # ### end Alembic commands ###
