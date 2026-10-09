"""add action types

Revision ID: 1492777a2dee
Revises: 028c0123ea58
Create Date: 2026-10-09 12:28:34.580465

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1492777a2dee"
down_revision: str | Sequence[str] | None = "028c0123ea58"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "action_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_action_types_id"), "action_types", ["id"], unique=False)
    with op.batch_alter_table("actions") as batch_op:
        batch_op.add_column(sa.Column("type_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_actions_type_id_action_types",
            "action_types",
            ["type_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    with op.batch_alter_table("actions") as batch_op:
        batch_op.drop_constraint("fk_actions_type_id_action_types", type_="foreignkey")
        batch_op.drop_column("type_id")
    op.drop_index(op.f("ix_action_types_id"), table_name="action_types")
    op.drop_table("action_types")
