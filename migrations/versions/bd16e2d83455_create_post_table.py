"""Create post table

Revision ID: bd16e2d83455
Revises: 10425b750690
Create Date: 2022-04-19 20:01:06.374715

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
import json

# revision identifiers, used by Alembic.
revision = 'bd16e2d83455'
down_revision = '10425b750690'
branch_labels = None
depends_on = None


def upgrade():
    posts = op.create_table(
        'posts',
        sa.Column('id', sa.BigInteger, primary_key=True, unique=True, index=True),
        sa.Column('reference_post_id', sa.BigInteger, ForeignKey("posts.id"), index=True, nullable=True),
        sa.Column('post_type', sa.String(10), nullable=False),
        sa.Column('text', sa.String(777), nullable=True),
        sa.Column('published_by', sa.BigInteger, ForeignKey("users.id"), index=True, nullable=False),
        sa.Column('published_at', sa.DateTime, nullable=False)           
    )

    with open("./migrations/seed/posts.json", "r") as f:
        data = json.loads(f.read())            
        op.bulk_insert(posts, data["posts"])   

def downgrade():
    op.drop_table('posts')



