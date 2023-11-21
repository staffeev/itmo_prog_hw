from core.models import db_session
from core.models.category import Category
from core.models.product import Product
from core.models.purchase import Purchase



if __name__ == "__main__":
    db_session.global_init("puchaces.db")
    session = db_session.create_session()
    p = session.query(Product).filter(Product.name == "prod1").first()
    print(p.categories)
    # c = Category(name="test1")
    # c2 = Category(name="test2")
    # c3 = Category(name="test3")
    # p1 = Product(name="prod1", cost=200)
    # p2 = Product(name="prod2", cost=300)
    # p1.categories.append(c)
    # p1.categories.append(c2)
    # p2.categories.append(c2)
    # p2.categories.append(c3)
    # session.add_all([c, c2, c3])
    # session.add_all([p1, p2])
    session.commit()
    session.close()