from flask_login import current_user
from sqlalchemy import update

from src.database import User


def check_current_user():
    if current_user.is_authenticated and current_user.is_superuser_or_is_staff():
        return True
    return False


def update_profile_image_stmt(
    image,
    name,
    surname,
    username,
    address,
    additional_address,
    country,
    user_id,
    address_conf,
    email_conf,
    phone_conf,
    is_staff,
    is_superuser,
):
    stmt = (
        update(User)
        .filter(User.user_id == user_id)
        .values(
            user_image=image.filename,
            name=name,
            surname=surname,
            username=username,
            address=address,
            additional_address=additional_address,
            country=country,
            address_confirmed=address_conf,
            email_confirmed=email_conf,
            phone_confirmed=phone_conf,
        )
    )
    return stmt


def update_profile_without_image_stmt(
    name,
    surname,
    username,
    address,
    additional_address,
    country,
    user_id,
    address_conf,
    email_conf,
    phone_conf,
    is_staff,
    is_superuser,
):
    stmt = (
        update(User)
        .filter(User.user_id == user_id)
        .values(
            name=name,
            surname=surname,
            username=username,
            address=address,
            additional_address=additional_address,
            country=country,
            address_confirmed=address_conf,
            email_confirmed=email_conf,
            phone_confirmed=phone_conf,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
    )
    return stmt


def check_address_conf(address_conf_1, address_conf_2):
    if address_conf_1 or address_conf_2:
        return True
    return False


def check_email_conf(email_conf):
    if email_conf == "on":
        return True
    return False


def check_phone_conf(phone_conf):
    if phone_conf == "on":
        return True
    return False


def check_is_staff(is_staff, is_superuser):
    if is_staff == "on" and is_superuser == "on":
        return True, True

    if is_staff == "on" and is_superuser != "on":
        return True, False

    if is_staff != "on" and is_superuser == "on":
        return False, True

    else:
        return False, False
