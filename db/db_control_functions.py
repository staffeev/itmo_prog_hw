import sys
import os
sys.path.append(os.getcwd())
from core.models import db_session
from core.models.purchase import Purchase
from core.models.product import Product
from core.models.category import Category


def wrap_with_session(make_commit=False):
    def __inner_func(func):
        def __inner_inner_func(*args, **kwargs):
            session = db_session.create_session()
            result = func(*args, **kwargs)
            if make_commit:
                session.commit()
            session.close()
            return result
        return __inner_inner_func
    return __inner_func


@wrap_with_session()
def load_products() -> list[Product]:
    """Возвращает данные о товарах из БД"""
    session = db_session.create_session()
    return session.query(Product).all()


@wrap_with_session()
def load_categories() -> list[Category]:
    """Возвращает данные о категориях из БД"""
    session = db_session.create_session()
    return session.query(Category).all()


@wrap_with_session(make_commit=True)
def add_category(category_name):
    """Создание новой категории"""
    session = db_session.create_session()
    category = Category(name=category_name)
    session.add(category)
    return True