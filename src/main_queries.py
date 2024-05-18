from sqlalchemy import insert

from src.database import Feedback, db


class MainQueries:

    @staticmethod
    def add_feedback_query(username, email, phone_number, message):
        try:
            if username and email and phone_number and message:
                stmt = (
                    insert(Feedback).values(username=username, email=email, phone_number=phone_number, message=message)
                )
                db.session.execute(stmt)
                db.session.commit()
                return "Ваше сообщение было отправлено, мы постараемся связаться с вами как можно скорее", True
            else:
                return "Необходимо заполнить все поля для отправки обращения", False
        except Exception as e:
            print(e)
            return "Ошибка отправки обращения, пожалуйста попробуйте позже", False
