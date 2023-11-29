import sys
import os
sys.path.append(os.getcwd())
from core.models import db_session
from core.models.product import Product
from core.models.category import Category
import datetime as dt


def get_products(session) -> list[Product]:
    """Возвращает данные о товарах из БД"""
    return session.query(Product).all()


def get_categories(session) -> list[Category]:
    """Возвращает данные о категориях из БД"""
    return session.query(Category).all()


def add_category(session, category_name: str) -> Category:
    """Создание новой категории"""
    category = Category(name=category_name)
    session.add(category)
    session.commit()
    return category


def get_category_by_name(session, category_name: str) -> Category:
    """Получение категории по ее имени"""
    category = session.query(Category).filter(Category.name == category_name).first()
    return category


def add_purchase(session, product_name: str, cost: float, is_usd: bool, 
                 date: dt.date, category: Category) -> Product:
    """Добавление новой покупки"""
    product = Product(name=product_name, cost=cost, is_usd=is_usd, date=date)
    product.categories.append(category)
    session.add(product)
    session.commit()
    return product