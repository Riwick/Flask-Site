import os.path
from decimal import Decimal

from sqlalchemy import select, insert, delete

from src.database import Product, db
from src.routes.utils import allowed_file, UPLOAD_FOLDER


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
    def add_product_query(title, short_desc, desc, price, cat_id, image):
        try:
            if not image:
                return "Для создания продукта необходимо загрузить изображение", False

            if image.filename == "":
                return "Для создания продукта необходимо загрузить изображение", False

            if image and allowed_file(image.filename):
                image.save(os.path.join(UPLOAD_FOLDER, image.filename))

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
                                       description=desc, price=my_decimal, category_id=cat_id, image=image.filename)
            )
            db.session.execute(stmt)
            db.session.commit()
            return "Продукт добавлен", True
        except Exception as e:
            print(e)
            return "Ошибка при добавлении продукта", False

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
