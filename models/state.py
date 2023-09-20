#!/usr/bin/python3
"""
This module defines a State class
"""
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.base_model import Base, BaseModel
from models.city import City


class State(BaseModel, Base):
    """
    This class represents a State Class
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """
            Getter for all city objects
            Returns:

            """
            city_list = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
