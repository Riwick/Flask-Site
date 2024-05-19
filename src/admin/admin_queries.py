from sqlalchemy import select, or_

from src.database import Product, Feedback, db, User


class AdminQueries:

    @staticmethod
    def get_3_last_products_for_main_page():
        query = (
            select(Product).order_by(Product.created_at.desc()).limit(3)
        )
        products = db.session.execute(query).scalars().all()
        return products

    @staticmethod
    def get_3_last_feedbacks_for_main_page():
        query = (
            select(Feedback).order_by(Feedback.feedback_id.desc()).limit(3)
        )
        feedbacks = db.session.execute(query).scalars().all()
        return feedbacks

    @staticmethod
    def get_all_products():
        query = (
            select(Product).order_by(Product.created_at.desc())
        )

        products = db.session.execute(query).scalars().all()
        return products

    @staticmethod
    def get_all_feedbacks():
        query = (
            select(Feedback).order_by(Feedback.feedback_id.desc())
        )

        feedbacks = db.session.execute(query).scalars().all()
        return feedbacks


class AdminUsersQueries:

    @staticmethod
    def get_all_users():
        query = (
            select(User)
        )
        users = db.session.execute(query).scalars().all()
        return users

    @staticmethod
    def get_all_staff_users():
        query = (
            select(User).filter(or_(User.is_staff, User.is_superuser))
        )
        users = db.session.execute(query).scalars().all()
        return users

    @staticmethod
    def get_3_last_users():
        query = (
            select(User).order_by(User.register_at.desc()).limit(3)
        )
        users = db.session.execute(query).scalars().all()
        return users

    @staticmethod
    def get_3_last_staff_users():
        query = (
            select(User).order_by(User.register_at.desc()).filter(or_(User.is_staff, User.is_superuser)).limit(3)
        )
        users = db.session.execute(query).scalars().all()
        return users
