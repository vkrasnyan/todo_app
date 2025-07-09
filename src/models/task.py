from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Integer, String, ForeignKey, Boolean, func, Text

from databases.database import Base

class Task(Base):
    """
    Модель задачи
    Attributes:
        id: int - идентификатор
        title: str - заголовок задачи
        description: str - описание задачи
        is_done: bool - флаг выполнения задачи
        owner_id: int - идентификатор пользователя,
                        создавшего заявку
        owner: User - связь с пользователем, создавшим заявку
    """
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id",
                   ondelete="CASCADE"),
                   nullable=False,
    )
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="tasks"
    )
