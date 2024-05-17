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


def get_paginated_products(products, page, per_page):
    paginated_products = None

    if page == 1:
        paginated_products = products[:per_page]
    if page == 2:
        paginated_products = products[per_page: per_page * page]
    if page > 2:
        paginated_products = products[per_page * (page - 1): (per_page * page) + per_page]

    return paginated_products


def get_total_basket_sum(basket):
    total_price = 0
    for product in basket.basket_products:
        total_price += product.price
    return total_price
