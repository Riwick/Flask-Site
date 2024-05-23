import os
from copy import deepcopy
from decimal import Decimal

from sqlalchemy import select, or_, delete, insert, update

from src.admin.utils import update_profile_without_image_stmt, update_profile_image_stmt
from src.database import Product, Feedback, db, User, Category, Country
from src.products.utils import PRODUCTS_UPLOAD_FOLDER
from src.users.users_utils import USER_UPLOAD_FOLDER
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
    def get_one_product_by_id(product_id: int):
        query = (
            select(Product).filter(Product.product_id == product_id)
        )
        product = db.session.execute(query).scalars().one_or_none()
        return product

    @staticmethod
    def delete_product(product_id: int):
        try:
            product = AdminProductsQueries.get_one_product_by_id(product_id)
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

                my_decimal = Decimal(str(price)).quantize(Decimal('0.01'))

                stmt = (
                    insert(Product).values(title=title, short_description=short_desc,
                                           description=desc, price=my_decimal, category_title=cat_name,
                                           image=image.filename)
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
            my_decimal = Decimal(str(price)).quantize(Decimal('0.01'))

            if not image or image.filename == "":
                stmt = (
                    update(Product).filter(Product.product_id == product_id).values(title=title,
                                                                                    short_description=short_desc,
                                                                                    description=desc, price=my_decimal,
                                                                                    category_title=cat_name)
                )
                db.session.execute(stmt)
                db.session.commit()

                return "Продукт обновлен", True

            if image and allowed_file(image.filename):
                stmt = (
                    update(Product).filter(Product.product_id == product_id).values(title=title,
                                                                                    short_description=short_desc,
                                                                                    description=desc, price=my_decimal,
                                                                                    category_title=cat_name,
                                                                                    image=image.filename)
                )
                db.session.execute(stmt)
                db.session.commit()

                os.remove(PRODUCTS_UPLOAD_FOLDER + product_image)
                image.save(os.path.join(PRODUCTS_UPLOAD_FOLDER, image.filename))

                return "Продукт обновлен", True

        except Exception as e:
            print(e)
            return "Ошибка при обновлении продукта", False


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

    @staticmethod
    def get_one_feedback_by_id(feedback_id):
        query = (
            select(Feedback).filter(Feedback.feedback_id == feedback_id)
        )
        fb = db.session.execute(query).scalars().one_or_none()
        return fb

    @staticmethod
    def delete_feedback(feedback_id: int):
        try:
            fb = AdminFeedbacksQueries.get_one_feedback_by_id(feedback_id)

            if fb:
                stmt = (
                    delete(Feedback).filter(Feedback.feedback_id == feedback_id)
                )
                db.session.execute(stmt)
                db.session.commit()
                return "Успешно удалено", True
            else:
                return "Такого обращения не существует", False
        except Exception as e:
            print(e)
            return "Во время удаления произошла ошибка", False


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

    @staticmethod
    def get_one_user_by_id(user_id):
        query = (
            select(User).filter(User.user_id == user_id)
        )
        user = db.session.execute(query).scalars().one_or_none()
        return user

    @staticmethod
    def update_user(image, name, surname, username, address, additional_address, country, user_id, address_conf,
                    email_conf, phone_conf, is_staff, is_superuser):
        try:
            user = AdminUsersQueries.get_one_user_by_id(user_id)
            last_user_image = deepcopy(user.user_image)
            if user:
                if last_user_image == image.filename or not image:
                    try:
                        stmt = update_profile_without_image_stmt(name, surname, username, address, additional_address,
                                                                 country, user_id, address_conf, email_conf, phone_conf,
                                                                 is_staff, is_superuser)
                        db.session.execute(stmt)
                        db.session.commit()
                        return "Профиль обновлен", True
                    except Exception as e:
                        db.session.rollback()
                        print(e)
                        return "Во время обновления профиля произошла ошибка", False

                if image and allowed_file(image.filename):
                    try:
                        stmt = update_profile_image_stmt(image, name, surname, username, address, additional_address,
                                                         country, user_id, address_conf, email_conf, phone_conf,
                                                         is_staff, is_superuser)
                        db.session.execute(stmt)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(e)
                        return "Во время обновления профиля произошла ошибка", False

                    image.save(os.path.join(USER_UPLOAD_FOLDER, image.filename))
                    os.remove(USER_UPLOAD_FOLDER + last_user_image)

                    return "Профиль обновлен", True
                else:
                    return "Выбранная вами фотография не может быть использована в качестве аватара", False
            else:
                return "Профиля такого пользователя не существует", False

        except Exception as e:
            print(e)
            return "Во время обновления профиля произошла ошибка", False


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
    def get_one_category_by_id(category_id):
        query = (
            select(Category).filter(Category.category_id == category_id)
        )
        category = db.session.execute(query).scalars().one_or_none()
        return category

    @staticmethod
    def delete_category_by_id(category_id: int):
        try:
            category = AdminCategoriesQueries.get_one_category_by_id(category_id)

            if category:
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
            categories = AdminCategoriesQueries.get_all_categories()

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

    @staticmethod
    def update_category(category_id, title, short_desc):
        try:
            category = AdminCategoriesQueries.get_one_category_by_id(category_id)

            if not category:
                return "Такой категории не существует", False

            stmt = (
                update(Category).filter(Category.category_id == category_id).values(title=title,
                                                                                    short_description=short_desc)
            )
            db.session.execute(stmt)
            db.session.commit()

            return "Категория обновлена", True

        except Exception as e:
            print(e)
            return "Ошибка при обновлении категории", False
