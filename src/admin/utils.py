from flask_login import current_user


def check_current_user():
    if current_user.is_authenticated and current_user.is_superuser_or_is_staff():
        return True
    return False
