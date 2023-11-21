from core.models import db_session
from core.models.category import Category
from core.models.product import Product
from core.models.purchase import Purchase
from datetime import datetime



def create_test1():
    c = Category(name="cat1")
    p = Product(name="prod1", cost=200)
    p.categories.append(c)
    session.add(c)
    session.add(p)


def create_test2():
    p = session.query(Product).first()
    pc = Purchase(product_id=p.id)
    pc.product = p
    session.add(pc)


def create_test3():
    pc = session.query(Purchase).first()
    print(pc.date, pc.product_id, pc.product)


def get_c():
    return session.query(Category).first()


def get_p():
    return session.query(Product).first()


def get_pc():
    return session.query(Purchase).first()




if __name__ == "__main__":
    db_session.global_init("puchaces.db")
    session = db_session.create_session()
    p = get_p()
    print(p.purchase.product.categories[0].products)
    # create_test3()
    session.commit()
    session.close()