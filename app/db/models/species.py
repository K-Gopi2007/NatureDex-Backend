from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    scientific_name = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(Text)
    image_url = Column(String)
