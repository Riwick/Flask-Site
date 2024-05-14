from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert

from src.database import db, User


class UserQueries:

    @staticmethod
    def create_user(username, password, email, phone):
        try:
            stmt = (
                insert(User).values(username=username, email=email, phone=phone, password=password)
            )
            db.session.execute(stmt)

            return "Вы успешно зарегистрированы", True

        except IntegrityError:
            return "Такой пользователь уже зарегистрирован", False

        except Exception as e:
            print(e)
            return "Во время регистрации произошла ошибка, попробуйте ещё раз позже", False
