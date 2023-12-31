"""empty message

Revision ID: 47d9d4385fc0
Revises: bfab3a2e2aa3
Create Date: 2023-06-09 18:17:21.074298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47d9d4385fc0'
down_revision = 'bfab3a2e2aa3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)

    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
        batch_op.alter_column('facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('website_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('website_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    # ### end Alembic commands ###
