"""create actions table

Revision ID: 49f7aa8d2c31
Revises: cbfd6becaf0d
Create Date: 2026-10-09 10:49:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "49f7aa8d2c31"
down_revision: Union[str, Sequence[str], None] = "cbfd6becaf0d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "actions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_actions_id"), "actions", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_actions_id"), table_name="actions")
    op.drop_table("actions")
