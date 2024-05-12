import datetime
from decimal import Decimal
from typing import Annotated

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text, DECIMAL, String, Numeric
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):

    repr_cols_num: int = 3
    repr_cols: tuple = ()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


db = SQLAlchemy(model_class=Base)

integer_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(default=datetime.datetime.utcnow)]


class Product(db.Model):
    product_id: Mapped[integer_pk]
    title: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    short_description: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
