from pydantic import BaseModel
from typing import Optional

class MapDiscoveryResponse(BaseModel):
    id: int
    species_id: int
    species_name: str
    location_lat: float
    location_lng: float
    discovered_at: str

class NearbySpeciesResponse(BaseModel):
    species_id: int
    species_name: str
    location_lat: float
    location_lng: float
