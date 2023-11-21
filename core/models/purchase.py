from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relation
from .db_session import SqlAlchemyBase
import datetime


class Purchase(SqlAlchemyBase):
    """Класс для ORM-модели покупки"""
    __tablename__ = "purchase"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.datetime.now)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relation("Product", uselist=False, back_populates="purchase",
                       cascade="all, delete")

    def __repr__(self):
        return f"Purchase(date={self.date.strftime('%d-%m-%Y')}, product_id={self.product_id})"
    
    def __str__(self):
        return repr(self)