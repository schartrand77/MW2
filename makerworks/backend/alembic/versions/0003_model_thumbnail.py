from alembic import op
import sqlalchemy as sa

revision = '0003_model_thumbnail'
down_revision = '0002_user_inventory'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('models_3d', sa.Column('thumbnail', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('models_3d', 'thumbnail')
