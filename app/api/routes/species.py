from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import SessionDep
from app.models.domain import Species
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class SpeciesResponse(BaseModel):
    id: int
    common_name: str
    scientific_name: str
    category: str
    habitat: Optional[str] = None
    distribution: Optional[str] = None
    conservation_status: Optional[str] = None
    diet: Optional[str] = None
    size: Optional[str] = None
    lifespan: Optional[str] = None

    class Config:
        from_attributes = True

@router.get("/", response_model=List[SpeciesResponse])
def get_all_species(db: SessionDep, limit: int = 100):
    species = db.query(Species).limit(limit).all()
    return species

@router.get("/compare", response_model=List[SpeciesResponse])
def compare_species(db: SessionDep, ids: str = Query(..., description="Comma separated species IDs")):
    try:
        id_list = [int(i.strip()) for i in ids.split(",")]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid IDs format")
    
    if len(id_list) < 2 or len(id_list) > 3:
        raise HTTPException(status_code=400, detail="Please provide 2 to 3 species IDs")

    species = db.query(Species).filter(Species.id.in_(id_list)).all()
    return species

@router.get("/{id}", response_model=SpeciesResponse)
def get_species_by_id(id: int, db: SessionDep):
    species = db.query(Species).filter(Species.id == id).first()
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    return species
