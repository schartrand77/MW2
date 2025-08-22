"""create notification subscription table"""

from alembic import op
import sqlalchemy as sa

revision = "0002_notifications"
down_revision = "0001_api_keys_webhooks"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "notification_subscriptions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("api_key_id", sa.Integer, sa.ForeignKey("api_keys.id"), nullable=False),
        sa.Column("event", sa.String(length=100), nullable=False),
        sa.Column("channel", sa.String(length=20), nullable=False),
        sa.Column("target", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("notification_subscriptions")
