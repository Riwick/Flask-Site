PRODUCTS_UPLOAD_FOLDER = "src/static/images/products_images/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename: str):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_user_register(username, password, password_confirm, email, phone):
    if password != password_confirm:
        return "Пароли не совпадают", False

    if username and phone and password and password == password_confirm and email:
        return "", True

    else:
        return "Для регистрации необходимо заполнить все поля", False


