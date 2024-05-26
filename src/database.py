import datetime
import enum
from decimal import Decimal
from typing import Annotated

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):

    repr_cols_num: int = 3
    repr_cols: tuple = ()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


db = SQLAlchemy(model_class=Base, engine_options={"echo": True})


integer_pk = Annotated[int, mapped_column(primary_key=True)]
not_nullable_int = Annotated[int, mapped_column(nullable=False)]

created_at = Annotated[
    datetime.datetime, mapped_column(default=datetime.datetime.utcnow)
]

not_nullable_str = Annotated[str, mapped_column(String(200), nullable=False)]
nullable_str = Annotated[str, mapped_column(String(200), nullable=True, default="")]

is_confirmed = Annotated[bool, mapped_column(default=False, nullable=True)]
is_staff = Annotated[bool, mapped_column(default=False)]


class Category(db.Model):
    category_id: Mapped[integer_pk]
    title: Mapped[str] = mapped_column(String(75), unique=True, nullable=False)
    short_description: Mapped[nullable_str]


class Product(db.Model):
    product_id: Mapped[integer_pk]
    title: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    short_description: Mapped[str] = mapped_column(String(255), nullable=True)
    image: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    price: Mapped[Decimal] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(default=0, nullable=True)

    category_title: Mapped[str] = mapped_column(
        ForeignKey("category.title", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[created_at]

    in_basket: Mapped[list["User"]] = relationship(
        back_populates="basket_products", secondary="basket"
    )

    in_favorites: Mapped[list["User"]] = relationship(
        back_populates="favorites_products", secondary="favorite"
    )

    repr_cols = ("description", "price", "category_title")


class Feedback(db.Model):
    feedback_id: Mapped[integer_pk]
    username: Mapped[not_nullable_str]
    email: Mapped[not_nullable_str]
    phone_number: Mapped[not_nullable_str]
    message: Mapped[not_nullable_str]


class Country(enum.Enum):
    Russia = "Россия"
    Belarus = "Беларусь"
    Kazakhstan = "Казахстан"
    Not_specified = "Не указано"


class User(db.Model):
    user_id: Mapped[integer_pk]
    name: Mapped[nullable_str]
    surname: Mapped[nullable_str]
    username: Mapped[not_nullable_str]

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    email_confirmed: Mapped[is_confirmed]

    phone: Mapped[str] = mapped_column(unique=True, nullable=False)
    phone_confirmed: Mapped[is_confirmed]

    address: Mapped[nullable_str]
    additional_address: Mapped[nullable_str]
    address_confirmed: Mapped[is_confirmed]

    country: Mapped["Country"] = mapped_column(
        nullable=True, default="country.Not_specified"
    )

    password: Mapped[not_nullable_str]

    user_image: Mapped[str] = mapped_column(
        default="default_user_avatar.jpg", nullable=False
    )
    register_at: Mapped[created_at]

    is_staff: Mapped[is_staff]
    is_superuser: Mapped[is_staff]

    basket_products: Mapped[list["Product"]] = relationship(
        back_populates="in_basket", secondary="basket"
    )

    favorites_products: Mapped[list["Product"]] = relationship(
        back_populates="in_favorites", secondary="favorite"
    )

    repr_cols = (
        "password",
        "register_at",
        "user_image",
        "phone",
        "name",
        "surname",
        "address",
    )


class Basket(db.Model):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.product_id", ondelete="CASCADE"), primary_key=True
    )


class Favorite(db.Model):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.product_id", ondelete="CASCADE"), primary_key=True
    )
