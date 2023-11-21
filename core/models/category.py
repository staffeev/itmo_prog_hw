from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relation, validates
from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    """Класс для ORM-модели категории товара"""
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    products = relation("Product", secondary="product_to_category", 
                        back_populates="categories", cascade="all, delete")

    @validates("name")
    def validate_name(self, _, value):
        """Проверка допустимых значений для имени"""
        if len(value) > 1000:
            raise ValueError("Name length can't be more than 1000 symbols")
        return value
    

    def __repr__(self):
        return f"Category(name={self.name})"
    
    def __str__(self):
        return repr(self)



    