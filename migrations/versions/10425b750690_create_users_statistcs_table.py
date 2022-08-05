"""Create users statistcs table

Revision ID: 10425b750690
Revises: ff902946565b
Create Date: 2022-04-19 15:33:30.152361

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
import json

# revision identifiers, used by Alembic.
revision = '10425b750690'
down_revision = 'ff902946565b'
branch_labels = None
depends_on = None


def upgrade():
    users_statistics = op.create_table(
        'users_statistics',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger,  ForeignKey('users.id'), nullable=False, unique=True),
        sa.Column('followee_counter', sa.BigInteger, nullable=False, default=0),
        sa.Column('follower_counter', sa.BigInteger, nullable=False, default=0),
        sa.Column('posts_counter', sa.BigInteger, nullable=False, default=0)
    )

    with open("./migrations/seed/users_statistics.json", "r") as f:
        data = json.loads(f.read())            
        op.bulk_insert(users_statistics, data["users_statistics"])      

def downgrade():
    op.drop_table('users_statistics')
