from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .species import Species

class DiscoveryBase(BaseModel):
    location_lat: Optional[str] = None
    location_lon: Optional[str] = None
    image_url: Optional[str] = None

class DiscoveryCreate(DiscoveryBase):
    species_id: int
    user_id: int

class Discovery(DiscoveryBase):
    id: int
    species_id: int
    user_id: int
    discovered_at: datetime
    species: Optional[Species] = None

    class Config:
        from_attributes = True
