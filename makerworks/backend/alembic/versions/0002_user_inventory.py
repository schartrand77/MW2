"""add user inventory table

Revision ID: 0002_user_inventory
Revises: 0001_initial
Create Date: 2024-06-07
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_user_inventory"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_inventory",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column(
            "product_variant_id",
            sa.String(),
            sa.ForeignKey("product_variants.id", ondelete="CASCADE"),
        ),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_table("user_inventory")
