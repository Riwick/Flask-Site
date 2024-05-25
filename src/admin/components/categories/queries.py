from sqlalchemy import select, delete, insert, update

from src.database import Category, db
from src.caching import cache, CATEGORIES_CACHE_TIME


class AdminCategoriesQueries:

    @staticmethod
    def get_3_last_categories_for_main_page():
        try:
            if cache.get("admin-3_last_categories_for_main_page"):
                return cache.get("admin-3_last_categories_for_main_page")
            query = select(Category).order_by(Category.category_id.desc()).limit(3)
            categories = db.session.execute(query).scalars().all()
            cache.set(
                "admin-3_last_categories_for_main_page",
                categories,
                CATEGORIES_CACHE_TIME,
            )
            return categories
        except Exception as e:
            print(e)

    @staticmethod
    def get_all_categories():
        try:
            if cache.get("admin-categories"):
                return cache.get("admin-categories")
            query = select(Category).order_by(Category.category_id.desc())
            categories = db.session.execute(query).scalars().all()
            cache.set("admin-categories", categories, CATEGORIES_CACHE_TIME)
            return categories
        except Exception as e:
            print(e)

    @staticmethod
    def get_one_category_by_id(category_id):
        try:
            if cache.get(f"admin-category {category_id}"):
                return cache.get(f"admin-category {category_id}")
            query = select(Category).filter(Category.category_id == category_id)
            category = db.session.execute(query).scalars().one_or_none()
            cache.set(f"admin-category {category_id}", category, CATEGORIES_CACHE_TIME)
            return category
        except Exception as e:
            print(e)

    @staticmethod
    def delete_category_by_id(category_id: int):
        try:
            category = AdminCategoriesQueries.get_one_category_by_id(category_id)

            if category:
                stmt = delete(Category).filter(Category.category_id == category_id)
                db.session.execute(stmt)
                db.session.commit()
                return "Успешно удалено", True
            else:
                return "Такой категории не существует", False
        except Exception as e:
            print(e)
            return "Во время удаления произошла ошибка", False

    @staticmethod
    def add_category(category_title: str, short_desc: str):
        try:
            categories = AdminCategoriesQueries.get_all_categories()

            for category in categories:
                if category.title == category_title:
                    return "Такая категория уже существует", False

            stmt = insert(Category).values(
                title=category_title, short_description=short_desc
            )
            db.session.execute(stmt)
            db.session.commit()

            return "Категория добавлена", True
        except Exception as e:
            print(e)
            return "Ошибка при добавлении категории", False

    @staticmethod
    def update_category(category_id, title, short_desc):
        try:
            category = AdminCategoriesQueries.get_one_category_by_id(category_id)

            if not category:
                return "Такой категории не существует", False

            stmt = (
                update(Category)
                .filter(Category.category_id == category_id)
                .values(title=title, short_description=short_desc)
            )
            db.session.execute(stmt)
            db.session.commit()

            return "Категория обновлена", True

        except Exception as e:
            print(e)
            return "Ошибка при обновлении категории", False
