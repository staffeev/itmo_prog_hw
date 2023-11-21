from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relation
from .db_session import SqlAlchemyBase


class Purchase(SqlAlchemyBase):
    """Класс для ORM-модели покупки"""
    __tablename__ = "purchase"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column()
    product = relation("Product", secondary="purchase_to_product", back_populates="purchase")