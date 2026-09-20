from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Discovery(Base):
    __tablename__ = "discoveries"

    id = Column(Integer, primary_key=True, index=True)
    species_id = Column(Integer, ForeignKey("species.id"))
    user_id = Column(Integer, index=True)
    discovered_at = Column(DateTime(timezone=True), server_default=func.now())
    location_lat = Column(String, nullable=True)
    location_lon = Column(String, nullable=True)
    image_url = Column(String)

    species = relationship("Species")
