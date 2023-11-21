from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relation
from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    """Класс для ORM-модели категории товара"""
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)