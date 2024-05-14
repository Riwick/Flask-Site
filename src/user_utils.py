from sqlalchemy import select

from src.database import User


USER_UPLOAD_FOLDER = "src/static/images/service_images/"


class UserLogin:

    def get_user_from_db(self, user_id, db):
        query = (
            select(User).filter(User.user_id == user_id)
        )
        self.__user = db.session.execute(query).scalars().one_or_none()
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.user_id)

    def get_image(self):
        return str(self.__user.user_image)

    def get_username(self):
        return str(self.__user.username)

    def get_phone_number(self):
        return str(self.__user.phone)

    def get_email(self):
        return str(self.__user.email)
