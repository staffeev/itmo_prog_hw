from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relation
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    """Класс для ORM-модели товара"""
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    cost = Column(Integer)
    category = relation("Category", secondary="product_to_category", back_populates="product")