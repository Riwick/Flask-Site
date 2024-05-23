from flask_paginate import Pagination


def get_pagination(total: list, page, per_page):
    pagination = Pagination(page=page, total=len(total),
                            per_page=per_page, display_msg="", alignment="center",
                            inner_window=1, outer_window=1, show_single_page=True, include_first_page_number=True)
    return pagination


PRODUCTS_UPLOAD_FOLDER = "src/products/static/images/products_images/"
