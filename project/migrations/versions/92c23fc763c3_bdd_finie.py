"""BDD finie

Revision ID: 92c23fc763c3
Revises: 
Create Date: 2019-01-12 18:13:17.502460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92c23fc763c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('File',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=24), nullable=True),
    sa.Column('path', sa.String(length=128), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('creationDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_File_creationDate'), 'File', ['creationDate'], unique=False)
    op.create_table('Folder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=24), nullable=True),
    sa.Column('creationDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Folder_creationDate'), 'Folder', ['creationDate'], unique=False)
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('hashPassword', sa.String(length=128), nullable=True),
    sa.Column('role', sa.Enum('user', 'admin', name='role'), nullable=True),
    sa.Column('creationDate', sa.DateTime(), nullable=True),
    sa.Column('locked', sa.Boolean(), nullable=True),
    sa.Column('failedLogin', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_User_creationDate'), 'User', ['creationDate'], unique=False)
    op.create_index(op.f('ix_User_email'), 'User', ['email'], unique=True)
    op.create_index(op.f('ix_User_username'), 'User', ['username'], unique=True)
    op.create_table('AccessFile',
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('fileId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fileId'], ['File.id'], ),
    sa.ForeignKeyConstraint(['userId'], ['User.id'], ),
    sa.PrimaryKeyConstraint('userId', 'fileId')
    )
    op.create_table('AccessFolder',
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('folderId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['folderId'], ['Folder.id'], ),
    sa.ForeignKeyConstraint(['userId'], ['User.id'], ),
    sa.PrimaryKeyConstraint('userId', 'folderId')
    )
    op.create_table('Log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['userId'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Log_date'), 'Log', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Log_date'), table_name='Log')
    op.drop_table('Log')
    op.drop_table('AccessFolder')
    op.drop_table('AccessFile')
    op.drop_index(op.f('ix_User_username'), table_name='User')
    op.drop_index(op.f('ix_User_email'), table_name='User')
    op.drop_index(op.f('ix_User_creationDate'), table_name='User')
    op.drop_table('User')
    op.drop_index(op.f('ix_Folder_creationDate'), table_name='Folder')
    op.drop_table('Folder')
    op.drop_index(op.f('ix_File_creationDate'), table_name='File')
    op.drop_table('File')
    # ### end Alembic commands ###
