from flask import Blueprint, render_template, redirect, flash, request
from flask_login import login_required
from flask_paginate import get_page_parameter

from src.admin.components.feedbacks.queries import AdminFeedbacksQueries
from src.admin.utils import check_current_user
from src.products.utils import get_pagination
from src.utils import get_paginated_staff, PER_PAGE

admin_feedbacks_router = Blueprint("admin_feedbacks_router", __name__)


@admin_feedbacks_router.route("/feedbacks")
@login_required
def all_feedbacks():
    if check_current_user():
        feedbacks = AdminFeedbacksQueries.get_all_feedbacks()

        page = request.args.get(get_page_parameter(), type=int, default=1)
        paginated_feedbacks = get_paginated_staff(page=page, staff=feedbacks, per_page=PER_PAGE)
        return render_template("admin/feedbacks/feedbacks.html", feedbacks=paginated_feedbacks,
                               title="Обращения", pagination=get_pagination(page=page, per_page=PER_PAGE,
                                                                            total=feedbacks))
    return redirect("/")


@admin_feedbacks_router.route("/feedbacks/<int:feedback_id>")
@login_required
def get_one_feedback(feedback_id: int):
    if check_current_user():

        feedback = AdminFeedbacksQueries.get_one_feedback_by_id(feedback_id)
        return render_template("admin/feedbacks/feedback-detail.html", fb=feedback)
    return redirect("/")


@admin_feedbacks_router.route("/feedbacks/<int:feedback_id>/delete", methods=["GET", "POST", "DELETE"])
@login_required
def delete_feedback(feedback_id: int):
    if check_current_user():
        detail, status = AdminFeedbacksQueries.delete_feedback(feedback_id)
        if status:
            flash(detail, category="success")
            return redirect(request.referrer)
        else:
            flash(detail, category="error")

    return redirect("/")
