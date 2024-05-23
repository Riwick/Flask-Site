from sqlalchemy import select, delete

from src.database import Product, db, Category


class ProductQueries:

    @staticmethod
    def get_all_products_query():
        try:
            query = (
                select(Product)
            )

            products = db.session.execute(query).scalars().all()
            return products
        except Exception as e:
            print(e)

    @staticmethod
    def get_one_product_query(product_id: int):
        try:
            query = (
                select(Product).filter(Product.product_id == product_id)
            )
            product = db.session.execute(query).scalars().one_or_none()
            return product
        except Exception as e:
            print(e)

    @staticmethod
    def get_all_categories():
        try:
            query = (
                select(Category).order_by(Category.title)
            )
            categories = db.session.execute(query).scalars().all()
            return categories
        except Exception as e:
            print(e)

    @staticmethod
    def get_products_by_category(category_title):
        try:
            query = (
                select(Product).filter(Product.category_title == category_title)
            )
            products = db.session.execute(query).scalars().all()
            return products
        except Exception as e:
            print(e)

    @staticmethod
    def get_sorted_products(order_by):
        query = (
            select(Product).order_by(order_by)
        )
        products = db.session.execute(query).scalars().all()
        return products