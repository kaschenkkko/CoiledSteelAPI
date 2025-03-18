from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, Integer

from ..core.database import Base


class CoiledSteel(Base):
    """Модель SQLAlchemy, представляющая рулонную сталь.

    Атрибуты:
        - id (int): Уникальный идентификатор рулона.
        - length (int): Длина рулона в метрах (обязательное поле, больше 0).
        - weight (int): Вес рулона в килограммах (обязательное поле, больше 0).
        - created_at (datetime): Дата и время создания записи о рулоне.
        - deleted_at (datetime | None): Дата и время удаления рулона. Может
          быть пустым.
    """

    __tablename__ = 'coiled_steel'

    id = Column(Integer, primary_key=True, index=True)
    length = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint('weight > 0', name='check_weight_positive'),
        CheckConstraint('length > 0', name='check_length_positive'),
    )
