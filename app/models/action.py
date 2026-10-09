from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    state: Mapped[str | None] = mapped_column(String(2), nullable=True, index=True)
    region: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    type_id: Mapped[int | None] = mapped_column(
        ForeignKey("action_types.id", ondelete="SET NULL"), nullable=True
    )