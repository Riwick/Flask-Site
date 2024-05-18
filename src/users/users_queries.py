import os
from copy import deepcopy

from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, delete, and_
from sqlalchemy.orm import selectinload

from src.database import db, User, Basket
from src.utils import allowed_file
from src.users.users_utils import USER_UPLOAD_FOLDER, update_profile_image_stmt, update_profile_without_image_stmt


class UserQueries:

    @staticmethod
    def create_user_query(username, password, email, phone):
        try:
            stmt = (
                insert(User).values(username=username, email=email, phone=phone, password=password)
            )
            db.session.execute(stmt)
            db.session.commit()

            return "Вы успешно зарегистрированы", True

        except IntegrityError:
            return "Такой пользователь уже зарегистрирован", False

        except Exception as e:
            print(e)
            return "Во время регистрации произошла ошибка, попробуйте ещё раз позже", False

    @staticmethod
    def select_user_by_email_query(email: str):
        try:
            query = (
                select(User).filter(User.email == email)
            )
            user = db.session.execute(query).scalars().all()

            if user:
                return user[0], True
            else:
                return None, False

        except Exception as e:
            print(e)
            return None, False

    @staticmethod
    def get_basket_products_query(user_id):
        query = (
            select(User).filter(User.user_id == user_id).options(selectinload(User.basket_products))
        )
        basket = db.session.execute(query).scalars().one_or_none()
        return basket

    @staticmethod
    def get_basket_query(user_id):
        query = (
            select(Basket).filter(Basket.user_id == user_id)
        )
        basket = db.session.execute(query).scalars().all()
        print(basket)
        return basket

    @staticmethod
    def delete_product_from_basket_query(user_id, product_id):
        try:
            query = (
                select(Basket).filter(and_(Basket.user_id == user_id, Basket.product_id == product_id))
            )

            product = db.session.execute(query).scalars().all()

            if not product:
                return "Вы ещё не добавили этот продукт в корзину", False

            stmt = (
                delete(Basket).filter(and_(Basket.user_id == user_id, Basket.product_id == product_id))
            )
            db.session.execute(stmt)
            db.session.commit()
            return "Успешно удалено", True
        except Exception as e:
            print(e)
            return "Ошибка при удалении продукта из корзины", False

    @staticmethod
    def add_product_to_basket_query(product_id, user_id):
        try:
            query = (
                select(Basket).filter(and_(Basket.user_id == user_id, Basket.product_id == product_id))
            )

            product = db.session.execute(query).scalars().all()
            if product:
                return "Этот продукт уже в вашей корзине, просто загляните туда :)", False
            stmt = (
                insert(Basket).values(user_id=user_id, product_id=product_id)
            )
            db.session.execute(stmt)
            db.session.commit()
            return "Добавлено", True
        except Exception as e:
            print(e)
            return "Ошибка при добавлении продукта в корзину", False

    @staticmethod
    def get_user_by_id(user_id):
        query = (
            select(User).filter(User.user_id == user_id)
        )
        user = db.session.execute(query).scalars().one_or_none()
        return user

    @staticmethod
    def update_profile_query(image, name, surname, username, address, additional_address, country, user_id):
        try:
            user = UserQueries.get_user_by_id(user_id)
            last_user_image = deepcopy(user.user_image)
            if user:
                if last_user_image == image.filename or not image:
                    try:
                        stmt = update_profile_without_image_stmt(name, surname, username, address,
                                                                 additional_address, country, user_id)
                        db.session.execute(stmt)
                        db.session.commit()
                        return "Профиль обновлен", True
                    except Exception as e:
                        print(e)
                        return "Во время обновления профиля произошла ошибка", False

                if image and allowed_file(image.filename):
                    try:
                        stmt = update_profile_image_stmt(image, name, surname, username, address,
                                                         additional_address, country, user_id)
                        db.session.execute(stmt)
                        db.session.commit()
                    except Exception as e:
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
