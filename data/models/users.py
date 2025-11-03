from sqlalchemy import JSON, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from typing import Dict

from .base import Base


class User(Base):

    __tablename__ = "Users"
    """
    Model for storing user accounts with validation.
    Typically used in the 'users' collection.
    """
    username: Mapped[str] = mapped_column(String(30), primary_key=True,
                                          nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    new_user: Mapped[bool] = mapped_column(Boolean, nullable=False,
                                           default=True)
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    permissions: Mapped[Dict[str, Dict[str, bool]]] = mapped_column(
                                                      JSON, nullable=False,
                                                      default=dict)
