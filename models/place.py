from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import getenv
from models.amenity import Amenity

if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column('place_id', String(60), ForeignKey('places.id'),
               primary_key=True, nullable=False),
        Column('amenity_id', String(60), ForeignKey('amenities.id'),
               primary_key=True, nullable=False)
    )

class Place(BaseModel, Base):
    """This class defines a place by various attributes"""
    __tablename__ = "places"
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey("cities.id"),
                         nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"),
                         nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False
        )
    else:
        @property
        def amenities(self):
            """Getter attribute that returns the list of Amenity instances
            based on the attribute amenity_ids"""
            from models import storage
            amenity_instances = []
            for amenity_id in self.amenity_ids:
                amenity_instance = storage.get(Amenity, amenity_id)
                if amenity_instance:
                    amenity_instances.append(amenity_instance)
            return amenity_instances

        @amenities.setter
        def amenities(self, amenity):
            """Setter attribute that handles append method for adding
            an Amenity.id to the attribute amenity_ids"""
            if isinstance(amenity, Amenity):
                self.amenity_ids.append(amenity.id)