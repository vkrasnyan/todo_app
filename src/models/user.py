from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer

from databases.database import Base

class User(Base):
    """Модель пользователя
    Attributes:
        id: int - идентификатор
        username: str - имя пользователя
        hashed_password: str - пароль пользователя
        tasks: List[Task] - связь с задачами пользователя
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
