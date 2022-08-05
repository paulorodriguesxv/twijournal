"""Create followers table

Revision ID: ff902946565b
Revises: 81445603f267
Create Date: 2022-04-19 07:40:34.607656

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
import json

# revision identifiers, used by Alembic.
revision = 'ff902946565b'
down_revision = '81445603f267'
branch_labels = None
depends_on = None


def upgrade():
    followers = op.create_table(
        'followers',
        sa.Column('followee_id', sa.BigInteger, ForeignKey('users.id'), nullable=False),
        sa.Column('follower_id', sa.BigInteger, ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        
        sa.UniqueConstraint('followee_id', 'follower_id', name='unique_follower')

    )

    with open("./migrations/seed/followers.json", "r") as f:
        data = json.loads(f.read())            
        op.bulk_insert(followers, data["followers"])   

def downgrade():
    op.drop_table('followers')
