from sqlalchemy import select

from src.database import Product, db, Category
from src.caching import cache


class ProductQueries:

    @staticmethod
    def get_all_products_query():
        try:
            if cache.get("all_products"):
                return cache.get("all_products")

            query = (
                select(Product)
            )

            products = db.session.execute(query).scalars().all()
            cache.set("all_products", products, 120)
            return products
        except Exception as e:
            print(e)

    @staticmethod
    def get_one_product_query(product_id: int):
        try:
            if cache.get(f"product {product_id}"):
                return cache.get(f"product {product_id}")
            query = (
                select(Product).filter(Product.product_id == product_id)
            )
            product = db.session.execute(query).scalars().one_or_none()
            cache.set(f"product {product_id}", product, 120)
            return product
        except Exception as e:
            print(e)

    @staticmethod
    def get_all_categories():
        try:
            if cache.get("categories"):
                return cache.get("categories")
            query = (
                select(Category).order_by(Category.title)
            )
            categories = db.session.execute(query).scalars().all()
            cache.set("categories", categories, 120)
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

