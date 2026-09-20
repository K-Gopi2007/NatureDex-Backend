from pydantic import BaseModel
from typing import Optional

class SpeciesBase(BaseModel):
    name: str
    scientific_name: str
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    habitat: Optional[str] = None
    distribution: Optional[str] = None
    conservation_status: Optional[str] = None
    diet: Optional[str] = None
    size: Optional[str] = None
    lifespan: Optional[str] = None

class SpeciesCreate(SpeciesBase):
    pass

class Species(SpeciesBase):
    id: int

    class Config:
        from_attributes = True
