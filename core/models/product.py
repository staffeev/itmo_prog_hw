from sqlalchemy import Column, Integer, ForeignKey, String, Table, Float
from sqlalchemy.orm import relation, validates
from .db_session import SqlAlchemyBase


association_table = Table(
    'product_to_category',
    SqlAlchemyBase.metadata,
    Column('product', Integer, ForeignKey('product.id')),
    Column('category', Integer, ForeignKey('category.id'))
)


class Product(SqlAlchemyBase):
    """Класс для ORM-модели товара"""
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    categories = relation("Category", secondary="product_to_category", 
                          back_populates="products")

    @validates("name")
    def validate_name(self, _, value):
        """Проверка допустимых значений для имени"""
        if len(value) > 1000:
            raise ValueError("Name length can't be more than 1000 symbols")
        return value

    @validates("cost")
    def validate_cost(self, _, value):
        """Проверка допустимых значений для цены"""
        if value < 0:
            raise ValueError("Cost must be positive float")
        if value > 9223372036854775807:
            raise ValueError("")
        if not 0 < value < 9223372036854775807:
            raise ValueError("Cost can't be so enormous")
        return value
    

    def __repr__(self):
        return f"Product(name={self.name}, cost={self.cost})"
    

    def __str__(self):
        return repr(self)