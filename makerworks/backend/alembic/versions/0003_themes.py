from alembic import op
import sqlalchemy as sa

revision = "0003_themes"
down_revision = "0002_notifications"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "themes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("org", sa.String(length=100), nullable=False, unique=True),
        sa.Column("tokens", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
    )


def downgrade() -> None:
    op.drop_table("themes")
