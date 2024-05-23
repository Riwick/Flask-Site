from flask import Blueprint, redirect, render_template, flash, request
from flask_login import login_required

from src.admin.components.feedbacks.queries import AdminFeedbacksQueries
from src.admin.components.users.queries import AdminUsersQueries
from src.admin.components.categories.queries import AdminCategoriesQueries
from src.admin.components.products.queries import AdminProductsQueries
from src.admin.utils import check_current_user, check_address_conf, check_email_conf, check_phone_conf, check_is_staff

from src.admin.components.categories.routes import admin_categories_router
from src.admin.components.products.routes import admin_product_router
from src.admin.components.users.routes import admin_users_router
from src.admin.components.feedbacks.routes import admin_feedbacks_router

admin_router = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin_router.route("/")
@login_required
def index():
    if check_current_user():
        products = AdminProductsQueries.get_3_last_products_for_main_page()
        feedbacks = AdminFeedbacksQueries.get_3_last_feedbacks_for_main_page()
        categories = AdminCategoriesQueries.get_3_last_categories_for_main_page()
        return render_template("admin/index.html",
                               products=products, feedbacks=feedbacks, categories=categories)
    return redirect("/")


"""Роуты продуктов"""

admin_router.register_blueprint(admin_product_router)

"""Роуты обратной связи"""

admin_router.register_blueprint(admin_feedbacks_router)

"""Роуты пользователей"""

admin_router.register_blueprint(admin_users_router)

"""Роуты категорий"""

admin_router.register_blueprint(admin_categories_router)
