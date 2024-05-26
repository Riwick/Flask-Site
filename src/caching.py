from flask_caching.backends import RedisCache
from flask_caching import Cache

cache = RedisCache(host="localhost", port=6379, db=1)
simple_cache = Cache(config={"CACHE_TYPE": "SimpleCache"})

PRODUCTS_CACHE_TIME = 60 * 60
CATEGORIES_CACHE_TIME = 60 * 10
FEEDBACKS_CACHE_TIME = 60 * 5
USERS_CACHE_TIME = 60 * 2
BASKET_CACHE_TIME = 60
FAVORITES_CACHE_TIME = 60


def delete_all_categories_cache(category_id):
    cache.delete("categories")
    cache.delete("admin-categories")
    cache.delete(f"admin-category {category_id}")
    cache.delete("admin-3_last_categories_for_main_page")


def delete_all_product_cache(product_id):
    cache.delete("all_products")
    cache.delete(f"product {product_id}")
    cache.delete("admin-products")
    cache.delete("admin-3_last_products_for_main_page")


def delete_all_feedback_cache(feedback_id):
    cache.delete("admin-3_last_feedbacks_for_main_page")
    cache.delete("admin-feedbacks")
    cache.delete(f"feedback {feedback_id}")


def delete_all_user_cache(user_id):
    cache.delete("admin-users")
    cache.delete("admin-staff_users")
    cache.delete("admin-3_last_users")
    cache.delete("admin-3_last_staff_users")
    cache.delete(f"user {user_id}")


def delete_all_user_cache_without_id():
    cache.delete("admin-users")
    cache.delete("admin-staff_users")
    cache.delete("admin-3_last_users")
    cache.delete("admin-3_last_staff_users")


def delete_all_basket_cache(user_id):
    cache.delete(f"basket {user_id}")
    cache.delete(f"basket_products {user_id}")
