from sqlalchemy import select, update
from flask_login import UserMixin

from src.database import User


USER_UPLOAD_FOLDER = "src/static/images/user_images/"


class UserLogin(UserMixin):
    __user = None

    def get_user_from_db(self, user_id, db):
        query = (
            select(User).filter(User.user_id == user_id)
        )
        self.__user = db.session.execute(query).scalars().one_or_none()
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_superuser_or_is_staff(self):
        return self.__user.is_superuser or self.__user.is_staff

    def get_id(self):
        return str(self.__user.user_id)

    def get_image(self):
        return str(self.__user.user_image)

    def get_username(self):
        return str(self.__user.username)

    def get_name(self):
        return str(self.__user.name)

    def get_surname(self):
        return str(self.__user.surname)

    def get_phone_number(self):
        return str(self.__user.phone)

    def get_email(self):
        return str(self.__user.email)

    def get_address(self):
        return str(self.__user.address)

    def get_additional_address(self):
        return str(self.__user.additional_address)

    def get_country(self):
        return str(self.__user.country).rsplit(".", 1)[1]


def update_profile_image_stmt(image, name, surname, username, address, additional_address, country, user_id):
    stmt = (
        update(User).filter(User.user_id == user_id)
        .values(user_image=image.filename, name=name, surname=surname, username=username,
                address=address, additional_address=additional_address, country=country)
    )
    return stmt


def update_profile_without_image_stmt(name, surname, username, address, additional_address, country, user_id):
    stmt = (
        update(User).filter(User.user_id == user_id)
        .values(name=name, surname=surname, username=username, address=address,
                additional_address=additional_address, country=country)
    )
    return stmt
