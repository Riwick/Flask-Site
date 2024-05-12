from decimal import Decimal

from sqlalchemy import select, insert

from src.database import Product, db


class ProductQueries:

    @staticmethod
    def get_all_products_query():
        query = (
            select(Product)
        )
        products = db.session.execute(query).scalars().all()
        return products

    @staticmethod
    def get_one_product_query(product_id: int):
        query = (
            select(Product).filter(Product.product_id == product_id)
        )
        product = db.session.execute(query).scalars().one_or_none()
        return product

    @staticmethod
    def add_product_query(title, short_desc, desc, price, cat_id):
        try:
            query = (
                select(Product)
            )
            products = db.session.execute(query).scalars().all()

            for product in products:
                if product.title == title:
                    return "Такой продукт уже существует", False
            my_decimal = Decimal(str(price)).quantize(Decimal('0.01'))

            stmt = (
                insert(Product).values(title=title, short_description=short_desc,
                                       description=desc, price=my_decimal, category_id=cat_id)
            )
            db.session.execute(stmt)
            db.session.commit()
            return "Продукт добавлен", True
        except:
            return "Ошибка при добавлении продукта", False
