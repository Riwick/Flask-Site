import os
from copy import deepcopy

from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, delete, and_
from sqlalchemy.orm import selectinload

from src.database import db, User, Basket, Favorite
from src.utils import allowed_file
from src.users.users_utils import (
    USER_UPLOAD_FOLDER,
    update_profile_image_stmt,
    update_profile_without_image_stmt,
)
from src.caching import cache, USERS_CACHE_TIME, BASKET_CACHE_TIME, FAVORITES_CACHE_TIME


class UserQueries:

    @staticmethod
    def create_user_query(username, password, email, phone):
        try:
            stmt = insert(User).values(
                username=username, email=email, phone=phone, password=password
            )
            db.session.execute(stmt)
            db.session.commit()

            return "Вы успешно зарегистрированы", True

        except IntegrityError:
            return "Такой пользователь уже зарегистрирован", False

        except Exception as e:
            print(e)
            return (
                "Во время регистрации произошла ошибка, попробуйте ещё раз позже",
                False,
            )

    @staticmethod
    def select_user_by_email_query(email: str):
        try:
            query = select(User).filter(User.email == email)
            user = db.session.execute(query).scalars().all()

            if user:
                return user[0], True
            else:
                return None, False

        except Exception as e:
            print(e)
            return None, False

    @staticmethod
    def get_user_by_id(user_id):
        try:
            if cache.get(f"user {user_id}"):
                return cache.get(f"user {user_id}")
            query = select(User).filter(User.user_id == user_id)
            user = db.session.execute(query).scalars().one_or_none()
            cache.set(f"user {user_id}", user, USERS_CACHE_TIME)
            return user
        except Exception as e:
            print(e)

    @staticmethod
    def update_profile_query(
        image, name, surname, username, address, additional_address, country, user_id
    ):
        try:
            user = UserQueries.get_user_by_id(user_id)
            last_user_image = deepcopy(user.user_image)
            if user:
                if last_user_image == image.filename or not image:
                    try:
                        stmt = update_profile_without_image_stmt(
                            name,
                            surname,
                            username,
                            address,
                            additional_address,
                            country,
                            user_id,
                        )
                        db.session.execute(stmt)
                        db.session.commit()
                        return "Профиль обновлен", True
                    except Exception as e:
                        print(e)
                        return "Во время обновления профиля произошла ошибка", False

                if image and allowed_file(image.filename):
                    try:
                        stmt = update_profile_image_stmt(
                            image,
                            name,
                            surname,
                            username,
                            address,
                            additional_address,
                            country,
                            user_id,
                        )
                        db.session.execute(stmt)
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        return "Во время обновления профиля произошла ошибка", False

                    image.save(os.path.join(USER_UPLOAD_FOLDER, image.filename))
                    os.remove(USER_UPLOAD_FOLDER + last_user_image)

                    return "Профиль обновлен", True
                else:
                    return (
                        "Выбранная вами фотография не может быть использована в качестве аватара",
                        False,
                    )
            else:
                return "Профиля такого пользователя не существует", False

        except Exception as e:
            print(e)
            return "Во время обновления профиля произошла ошибка", False


class UserBasketQueries:

    @staticmethod
    def get_basket_products_query(user_id):
        try:
            if cache.get(f"basket_products {user_id}"):
                return cache.get(f"basket_products {user_id}")
            query = (
                select(User)
                .filter(User.user_id == user_id)
                .options(selectinload(User.basket_products))
            )
            basket = db.session.execute(query).scalars().one_or_none()
            cache.set(f"basket_products {user_id}", basket, BASKET_CACHE_TIME)
            return basket
        except Exception as e:
            print(e)

    @staticmethod
    def get_basket_query(user_id):
        try:
            if cache.get(f"basket {user_id}"):
                return cache.get(f"basket {user_id}")
            query = select(Basket).filter(Basket.user_id == user_id)
            basket = db.session.execute(query).scalars().all()
            cache.set(f"basket {user_id}", basket, BASKET_CACHE_TIME)
            return basket
        except Exception as e:
            print(e)

    @staticmethod
    def delete_product_from_basket_query(user_id, product_id):
        try:
            query = select(Basket).filter(
                and_(Basket.user_id == user_id, Basket.product_id == product_id)
            )

            product = db.session.execute(query).scalars().all()

            if not product:
                return "Вы ещё не добавили этот продукт в корзину", False

            stmt = delete(Basket).filter(
                and_(Basket.user_id == user_id, Basket.product_id == product_id)
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
            query = select(Basket).filter(
                and_(Basket.user_id == user_id, Basket.product_id == product_id)
            )

            product = db.session.execute(query).scalars().all()
            if product:
                return (
                    "Этот продукт уже в вашей корзине, просто загляните туда :)",
                    False,
                )
            stmt = insert(Basket).values(user_id=user_id, product_id=product_id)
            db.session.execute(stmt)
            db.session.commit()
            return "Добавлено", True
        except Exception as e:
            print(e)
            return "Ошибка при добавлении продукта в корзину", False


class UserFavoritesQuery:

    @staticmethod
    def get_favorites_products_query(user_id):
        try:
            if cache.get(f"favorites_products {user_id}"):
                return cache.get(f"favorites_products {user_id}")
            query = (
                select(User)
                .filter(User.user_id == user_id)
                .options(selectinload(User.favorites_products))
            )
            fv = db.session.execute(query).scalars().one_or_none()
            cache.set(f"favorites_products {user_id}", fv, FAVORITES_CACHE_TIME)
            return fv
        except Exception as e:
            print(e)

    @staticmethod
    def get_favorites_query(user_id):
        try:
            if cache.get(f"favorites {user_id}"):
                return cache.get(f"favorites {user_id}")
            query = select(Favorite).filter(Favorite.user_id == user_id)
            fv = db.session.execute(query).scalars().all()
            cache.set(f"favorites {user_id}", fv, FAVORITES_CACHE_TIME)
            return fv
        except Exception as e:
            print(e)

    @staticmethod
    def delete_product_from_favorites_query(user_id, product_id):
        try:
            query = select(Favorite).filter(
                and_(Favorite.user_id == user_id, Favorite.product_id == product_id)
            )

            product = db.session.execute(query).scalars().all()

            if not product:
                return "Вы ещё не добавили этот продукт в избранное", False

            stmt = delete(Favorite).filter(
                and_(Favorite.user_id == user_id, Favorite.product_id == product_id)
            )
            db.session.execute(stmt)
            db.session.commit()
            return "Успешно удалено", True
        except Exception as e:
            print(e)
            return "Ошибка при удалении продукта из избранного", False

    @staticmethod
    def add_product_to_favorites_query(product_id, user_id):
        try:
            query = select(Favorite).filter(
                and_(Favorite.user_id == user_id, Favorite.product_id == product_id)
            )

            product = db.session.execute(query).scalars().all()
            if product:
                return (
                    "Этот продукт уже в вашем избранном, просто загляните туда :)",
                    False,
                )
            stmt = insert(Favorite).values(user_id=user_id, product_id=product_id)
            db.session.execute(stmt)
            db.session.commit()
            return "Добавлено", True
        except Exception as e:
            print(e)
            return "Ошибка при добавлении продукта в избранное", False
