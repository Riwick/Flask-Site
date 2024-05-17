from flask_paginate import Pagination

PRODUCTS_UPLOAD_FOLDER = "src/static/images/products_images/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename: str):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_pagination(total: list, page, per_page):
    pagination = Pagination(page=page, total=len(total),
                            per_page=per_page, display_msg="", alignment="center",
                            inner_window=1, outer_window=1, show_single_page=True, include_first_page_number=True)
    return pagination
