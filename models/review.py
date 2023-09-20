#!/usr/bin/python3
"""
This module defines a Review class
"""
from sqlalchemy import ForeignKey, String, Column

from models.base_model import Base, BaseModel


class Review(BaseModel, Base):
    """
    This class represents a Review class
    """
    __tablename__ = "reviews"
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
