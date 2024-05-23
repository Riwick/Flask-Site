ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename: str):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_paginated_staff(staff, page, per_page):
    paginated_staff = None

    if page == 1:
        paginated_staff = staff[:per_page]
    if page == 2:
        paginated_staff = staff[per_page: per_page * page]
    if page > 2:
        paginated_staff = staff[per_page * (page - 1): (per_page * page) + per_page]

    return paginated_staff


PER_PAGE = 10
