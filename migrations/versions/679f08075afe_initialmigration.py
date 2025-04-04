"""initialmigration

Revision ID: 679f08075afe
Revises: 
Create Date: 2025-03-29 02:41:26.290412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '679f08075afe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('donor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('blood_type', sa.String(length=5), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('availability_status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('hospital',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('contact_number', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blood_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('contact_number', sa.String(length=20), nullable=False),
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.Column('blood_type', sa.String(length=5), nullable=False),
    sa.Column('units_needed', sa.Integer(), nullable=False),
    sa.Column('urgency_level', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospital.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('donation_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('donor_id', sa.Integer(), nullable=False),
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.Column('blood_type', sa.String(length=5), nullable=False),
    sa.Column('donated_at', sa.DateTime(), nullable=True),
    sa.Column('next_eligible_donation', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['donor_id'], ['donor.id'], ),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospital.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('donor_match',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request_id', sa.Integer(), nullable=False),
    sa.Column('donor_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('Notified', 'Accepted', 'Rejected', 'Completed', name='match_status'), nullable=True),
    sa.Column('notified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['donor_id'], ['donor.id'], ),
    sa.ForeignKeyConstraint(['request_id'], ['blood_request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('donor_id', sa.Integer(), nullable=False),
    sa.Column('request_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('status', sa.Enum('Sent', 'Delivered', 'Failed', name='notification_status'), nullable=True),
    sa.Column('sent_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['donor_id'], ['donor.id'], ),
    sa.ForeignKeyConstraint(['request_id'], ['blood_request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notification')
    op.drop_table('donor_match')
    op.drop_table('donation_record')
    op.drop_table('blood_request')
    op.drop_table('hospital')
    op.drop_table('donor')
    # ### end Alembic commands ###
