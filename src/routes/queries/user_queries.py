from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select

from src.database import db, User


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
