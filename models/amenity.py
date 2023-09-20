#!/usr/bin/python3
"""
This module defines an Amenity class
"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel


class Amenity(BaseModel, Base):
    """
    This module represent an Amenity class
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity",
                                   viewonly=False)
