"""create user table

Revision ID: 81445603f267
Revises: 
Create Date: 2022-01-30 14:03:06.790912

"""
import json
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '81445603f267'
down_revision = None
branch_labels = None
depends_on = None

import logging
def upgrade():
    users = op.create_table(
        'users',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(14), nullable=False, unique=True, index=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )

    with open("./migrations/seed/users.json", "r") as f:
        data = json.loads(f.read())            
        op.bulk_insert(users, data["users"])        

        
def downgrade():
    op.drop_table('users')
