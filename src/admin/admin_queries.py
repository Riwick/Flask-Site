import os
from decimal import Decimal

from sqlalchemy import select, or_, delete, insert

from src.database import Product, Feedback, db, User, Category
from src.products.utils import PRODUCTS_UPLOAD_FOLDER
from src.utils import allowed_file


class AdminProductsQueries:

    @staticmethod
    def get_3_last_products_for_main_page():
        query = (
            select(Product).order_by(Product.created_at.desc()).limit(3)
        )
        products = db.session.execute(query).scalars().all()
        return products

    @staticmethod
    def get_all_products():
        query = (
            select(Product).order_by(Product.created_at.desc())
        )

        products = db.session.execute(query).scalars().all()
        return products

    @staticmethod
    def delete_product(product_id: int):
        try:
            query = (
                select(Product).filter(Product.product_id == product_id)
            )
            product = db.session.execute(query).scalars().one_or_none()
            if product:
                stmt = (
                    delete(Product).filter(Product.product_id == product_id)
                )
                db.session.execute(stmt)
                db.session.commit()
                return "Успешно удалено", True
            else:
                return "Такого продукта не существует", False
        except Exception as e:
            print(e)
            return "Во время удаления произошла ошибка", False

    @staticmethod
    def add_product_query(title, short_desc, desc, price, cat_name, image):
        try:
            if not image:
                return "Для создания продукта необходимо загрузить изображение", False

            if image.filename == "":
                return "Для создания продукта необходимо загрузить изображение", False

            if image and allowed_file(image.filename):
                image.save(os.path.join(PRODUCTS_UPLOAD_FOLDER, image.filename))

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
                                       description=desc, price=my_decimal, category_title=cat_name,
                                       image=image.filename)
            )
            db.session.execute(stmt)
            db.session.commit()

            return "Продукт добавлен", True

        except Exception as e:
            print(e)
            return "Ошибка при добавлении продукта", False


class AdminFeedbacksQueries:

    @staticmethod
    def get_3_last_feedbacks_for_main_page():
        query = (
            select(Feedback).order_by(Feedback.feedback_id.desc()).limit(3)
        )
        feedbacks = db.session.execute(query).scalars().all()
        return feedbacks

    @staticmethod
    def get_all_feedbacks():
        query = (
            select(Feedback).order_by(Feedback.feedback_id.desc())
        )

        feedbacks = db.session.execute(query).scalars().all()
        return feedbacks


class AdminUsersQueries:

    @staticmethod
    def get_all_users():
        query = (
            select(User)
        )
        users = db.session.execute(query).scalars().all()
        return users

    @staticmethod
    def get_all_staff_users():
        query = (
            select(User).filter(or_(User.is_staff, User.is_superuser))
        )
        users = db.session.execute(query).scalars().all()
        return users

    @staticmethod
    def get_3_last_users():
        query = (
            select(User).order_by(User.register_at.desc()).limit(3)
        )
        users = db.session.execute(query).scalars().all()
        return users

    @staticmethod
    def get_3_last_staff_users():
        query = (
            select(User).order_by(User.register_at.desc()).filter(or_(User.is_staff, User.is_superuser)).limit(3)
        )
        users = db.session.execute(query).scalars().all()
        return users


class AdminCategoriesQueries:

    @staticmethod
    def get_3_last_categories_for_main_page():
        query = (
            select(Category).order_by(Category.category_id.desc()).limit(3)
        )
        categories = db.session.execute(query).scalars().all()
        return categories

    @staticmethod
    def get_all_categories():
        query = (
            select(Category).order_by(Category.category_id.desc())
        )
        categories = db.session.execute(query).scalars().all()
        return categories

    @staticmethod
    def delete_category_by_id(category_id: int):
        try:
            query = (
                select(Category).filter(Category.category_id == category_id)
            )
            product = db.session.execute(query).scalars().one_or_none()
            if product:
                stmt = (
                    delete(Category).filter(Category.category_id == category_id)
                )
                db.session.execute(stmt)
                db.session.commit()
                return "Успешно удалено", True
            else:
                return "Такой категории не существует", False
        except Exception as e:
            print(e)
            return "Во время удаления произошла ошибка", False

    @staticmethod
    def add_category(category_title: str, short_desc: str):
        try:
            query = (
                select(Category)
            )
            categories = db.session.execute(query).scalars().all()

            for category in categories:
                if category.title == category_title:
                    return "Такая категория уже существует", False

            stmt = (
                insert(Category).values(title=category_title, short_description=short_desc)
            )
            db.session.execute(stmt)
            db.session.commit()

            return "Категория добавлена", True
        except Exception as e:
            print(e)
            return "Ошибка при добавлении категории", False
