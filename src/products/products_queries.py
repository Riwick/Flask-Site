import os.path
from decimal import Decimal

from sqlalchemy import select, insert, delete

from src.database import Product, db, Category
from src.utils import allowed_file
from src.products.utils import PRODUCTS_UPLOAD_FOLDER


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
    def delete_product_query(product_id):
        try:
            stmt = (
                delete(Product).filter(Product.product_id == product_id)
            )
            db.session.execute(stmt)
            db.session.commit()
            return "Продукт был удалён", True
        except Exception as e:
            print(e)
            return "Ошибка удаления продукта", False

    @staticmethod
    def get_all_categories():
        query = (
            select(Category)
        )
        categories = db.session.execute(query).scalars().all()
        return categories

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

