"""Create post daily control table

Revision ID: 2d324ae9bc42
Revises: bd16e2d83455
Create Date: 2022-04-20 11:42:47.915395

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
import json

# revision identifiers, used by Alembic.
revision = '2d324ae9bc42'
down_revision = 'bd16e2d83455'
branch_labels = None
depends_on = None


def upgrade():
    posts_statistics = op.create_table(
        'posts_statistics',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger,  ForeignKey('users.id'), nullable=False),
        sa.Column('year', sa.Integer, nullable=False),
        sa.Column('year_day', sa.Integer, nullable=False),
        sa.Column('post_counter', sa.BigInteger, nullable=False, default=0),
        sa.UniqueConstraint('user_id', 'year', 'year_day', name='unique_entry_by_user')
    )

    with open("./migrations/seed/posts_statistics.json", "r") as f:
        data = json.loads(f.read())            
        op.bulk_insert(posts_statistics, data["posts_statistics"])        

def downgrade():
    op.drop_table('posts_statistics')
