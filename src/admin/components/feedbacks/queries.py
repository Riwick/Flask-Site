from sqlalchemy import select, delete

from src.database import Feedback, db


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
