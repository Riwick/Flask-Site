from flask import Blueprint, render_template, redirect, flash, request
from flask_login import login_required

from src.admin.components.feedbacks.queries import AdminFeedbacksQueries
from src.admin.utils import check_current_user

admin_feedbacks_router = Blueprint("admin_feedbacks_router", __name__)


@admin_feedbacks_router.route("/feedbacks")
@login_required
def all_feedbacks():
    if check_current_user():
        feedbacks = AdminFeedbacksQueries.get_all_feedbacks()
        return render_template("admin/feedbacks/feedbacks.html",
                               feedbacks=feedbacks, title="Обращения")
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
