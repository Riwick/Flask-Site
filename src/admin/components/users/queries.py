import os
from copy import deepcopy

from sqlalchemy import select, or_

from src.admin.utils import update_profile_without_image_stmt, update_profile_image_stmt
from src.database import User, db
from src.users.users_utils import USER_UPLOAD_FOLDER
from src.utils import allowed_file


class AdminUsersQueries:

    @staticmethod
    def get_all_users():
        try:
            query = (
                select(User)
            )
            users = db.session.execute(query).scalars().all()
            return users
        except Exception as e:
            print(e)

    @staticmethod
    def get_all_staff_users():
        try:
            query = (
                select(User).filter(or_(User.is_staff, User.is_superuser))
            )
            users = db.session.execute(query).scalars().all()
            return users
        except Exception as e:
            print(e)

    @staticmethod
    def get_3_last_users():
        try:
            query = (
                select(User).order_by(User.register_at.desc()).limit(3)
            )
            users = db.session.execute(query).scalars().all()
            return users
        except Exception as e:
            print(e)

    @staticmethod
    def get_3_last_staff_users():
        try:
            query = (
                select(User).order_by(User.register_at.desc()).filter(or_(User.is_staff, User.is_superuser)).limit(3)
            )
            users = db.session.execute(query).scalars().all()
            return users
        except Exception as e:
            print(e)

    @staticmethod
    def get_one_user_by_id(user_id):
        try:
            query = (
                select(User).filter(User.user_id == user_id)
            )
            user = db.session.execute(query).scalars().one_or_none()
            return user
        except Exception as e:
            print(e)

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
