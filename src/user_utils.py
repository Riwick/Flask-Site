from sqlalchemy import select
from flask_login import UserMixin

from src.database import User


USER_UPLOAD_FOLDER = "src/static/images/service_images/"


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
        return str(self.__user.country)


def validate_user_register(username, password, password_confirm, email, phone):
    if password != password_confirm:
        return "Пароли не совпадают", False

    if username and phone and password and password == password_confirm and email:
        return "", True

    else:
        return "Для регистрации необходимо заполнить все поля", False
