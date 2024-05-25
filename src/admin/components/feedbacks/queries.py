from sqlalchemy import select, delete

from src.database import Feedback, db
from src.caching import cache, FEEDBACKS_CACHE_TIME


class AdminFeedbacksQueries:

    @staticmethod
    def get_3_last_feedbacks_for_main_page():
        try:
            if cache.get("admin-3_last_feedbacks_for_main_page"):
                return cache.get("admin-3_last_feedbacks_for_main_page")
            query = select(Feedback).order_by(Feedback.feedback_id.desc()).limit(3)
            feedbacks = db.session.execute(query).scalars().all()
            cache.set(
                "admin-3_last_feedbacks_for_main_page", feedbacks, FEEDBACKS_CACHE_TIME
            )
            return feedbacks
        except Exception as e:
            print(e)

    @staticmethod
    def get_all_feedbacks():
        try:
            if cache.get("admin-feedbacks"):
                return cache.get("admin-feedbacks")
            query = select(Feedback).order_by(Feedback.feedback_id.desc())

            feedbacks = db.session.execute(query).scalars().all()
            cache.set("admin-feedbacks", feedbacks, FEEDBACKS_CACHE_TIME)
            return feedbacks
        except Exception as e:
            print(e)

    @staticmethod
    def get_one_feedback_by_id(feedback_id):
        try:
            if cache.get(f"feedback {feedback_id}"):
                return cache.get(f"feedback {feedback_id}")
            query = select(Feedback).filter(Feedback.feedback_id == feedback_id)
            fb = db.session.execute(query).scalars().one_or_none()
            cache.set(f"feedback {feedback_id}", fb, FEEDBACKS_CACHE_TIME)
            return fb
        except Exception as e:
            print(e)

    @staticmethod
    def delete_feedback(feedback_id: int):
        try:
            fb = AdminFeedbacksQueries.get_one_feedback_by_id(feedback_id)

            if fb:
                stmt = delete(Feedback).filter(Feedback.feedback_id == feedback_id)
                db.session.execute(stmt)
                db.session.commit()
                return "Успешно удалено", True
            else:
                return "Такого обращения не существует", False
        except Exception as e:
            print(e)
            return "Во время удаления произошла ошибка", False
