import os
from copy import deepcopy
from decimal import Decimal

from sqlalchemy import select, delete, insert, update

from src.database import Product, db
from src.products.utils import PRODUCTS_UPLOAD_FOLDER
from src.utils import allowed_file
from src.caching import cache, PRODUCTS_CACHE_TIME


class AdminProductsQueries:

    @staticmethod
    def get_3_last_products_for_main_page():
        try:
            if cache.get("admin-3_last_products_for_main_page"):
                return cache.get("admin-3_last_products_for_main_page")
            query = select(Product).order_by(Product.created_at.desc()).limit(3)
            products = db.session.execute(query).scalars().all()
            cache.set(
                "admin-3_last_products_for_main_page", products, PRODUCTS_CACHE_TIME
            )
            return products
        except Exception as e:
            print(e)

    @staticmethod
    def get_all_products():
        try:
            if cache.get("admin-products"):
                return cache.get("admin-products")
            query = select(Product).order_by(Product.created_at.desc())

            products = db.session.execute(query).scalars().all()
            cache.set("admin-products", products, PRODUCTS_CACHE_TIME)
            return products
        except Exception as e:
            print(e)

    @staticmethod
    def get_one_product_by_id(product_id: int):
        try:
            if cache.get(f"product {product_id}"):
                return cache.get(f"product {product_id}")
            query = select(Product).filter(Product.product_id == product_id)
            product = db.session.execute(query).scalars().one_or_none()
            cache.set(f"product {product_id}", product, PRODUCTS_CACHE_TIME)
            return product
        except Exception as e:
            print(e)

    @staticmethod
    def delete_product(product_id: int):
        try:
            product = AdminProductsQueries.get_one_product_by_id(product_id)
            if product:
                stmt = delete(Product).filter(Product.product_id == product_id)
                db.session.execute(stmt)
                db.session.commit()
                return "Успешно удалено", True
            else:
                return "Такого продукта не существует", False
        except Exception as e:
            print(e)
            return "Во время удаления произошла ошибка", False

    @staticmethod
    def add_product(title, short_desc, desc, price, cat_name, image):
        try:
            if not image:
                return "Для создания продукта необходимо загрузить изображение", False

            if image.filename == "":
                return "Для создания продукта необходимо загрузить изображение", False

            if image and allowed_file(image.filename):

                products = AdminProductsQueries.get_all_products()

                for product in products:
                    if product.title == title:
                        return "Такой продукт уже существует", False

                my_decimal = Decimal(str(price)).quantize(Decimal("0.01"))

                stmt = insert(Product).values(
                    title=title,
                    short_description=short_desc,
                    description=desc,
                    price=my_decimal,
                    category_title=cat_name,
                    image=image.filename,
                )
                db.session.execute(stmt)
                db.session.commit()

                image.save(os.path.join(PRODUCTS_UPLOAD_FOLDER, image.filename))
                return "Продукт добавлен", True

        except Exception as e:
            print(e)
            return "Ошибка при добавлении продукта", False

    @staticmethod
    def update_product(product_id, title, short_desc, desc, price, cat_name, image):
        try:
            product = AdminProductsQueries.get_one_product_by_id(product_id)

            if not product:
                return "Такого продукта не существует", False

            product_image = deepcopy(product.image)
            my_decimal = Decimal(str(price)).quantize(Decimal("0.01"))

            if not image or image.filename == "":
                stmt = (
                    update(Product)
                    .filter(Product.product_id == product_id)
                    .values(
                        title=title,
                        short_description=short_desc,
                        description=desc,
                        price=my_decimal,
                        category_title=cat_name,
                    )
                )
                db.session.execute(stmt)
                db.session.commit()

                return "Продукт обновлен", True

            if image and allowed_file(image.filename):
                stmt = (
                    update(Product)
                    .filter(Product.product_id == product_id)
                    .values(
                        title=title,
                        short_description=short_desc,
                        description=desc,
                        price=my_decimal,
                        category_title=cat_name,
                        image=image.filename,
                    )
                )
                db.session.execute(stmt)
                db.session.commit()

                os.remove(PRODUCTS_UPLOAD_FOLDER + product_image)
                image.save(os.path.join(PRODUCTS_UPLOAD_FOLDER, image.filename))

                return "Продукт обновлен", True

        except Exception as e:
            print(e)
            return "Ошибка при обновлении продукта", False
