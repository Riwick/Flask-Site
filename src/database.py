from typing import Annotated

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)

integer_pk = Annotated[int, mapped_column(primary_key=True)]


