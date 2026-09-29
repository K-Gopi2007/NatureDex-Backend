from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.deps import SessionDep, get_current_user
from app.models.domain import User, Discovery, Species
from app.services.progression_service import ProgressionService

router = APIRouter()

class DiscoverySaveRequest(BaseModel):
    common_name: str
    scientific_name: str
    category: str
    description: Optional[str] = None
    conservation_status: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None

class DiscoveryResponse(BaseModel):
    id: int
    name: str
    scientificName: str
    category: str
    imageUrl: Optional[str] = None
    discoveredAt: str

@router.get("/", response_model=List[DiscoveryResponse])
def get_discoveries(db: SessionDep, current_user: User = Depends(get_current_user)):
    discoveries = db.query(Discovery).filter(Discovery.user_id == current_user.id).order_by(Discovery.discovered_at.desc()).all()
    result = []
    for d in discoveries:
        result.append({
            "id": d.id,
            "name": d.species.common_name or d.species.scientific_name,
            "scientificName": d.species.scientific_name,
            "category": d.species.category,
            "imageUrl": None,
            "discoveredAt": d.discovered_at.isoformat()
        })
    return result

@router.post("/", response_model=DiscoveryResponse)
def create_discovery(req: DiscoverySaveRequest, db: SessionDep, current_user: User = Depends(get_current_user)):
    # Find or create species
    species = db.query(Species).filter(Species.scientific_name == req.scientific_name).first()
    if not species:
        species = Species(
            common_name=req.common_name,
            scientific_name=req.scientific_name,
            category=req.category,
            description=req.description,
            conservation_status=req.conservation_status
        )
        db.add(species)
        db.commit()
        db.refresh(species)

    # Create discovery
    discovery = Discovery(
        user_id=current_user.id,
        species_id=species.id,
        location_lat=req.location_lat,
        location_lng=req.location_lng
    )
    db.add(discovery)
    db.commit()
    db.refresh(discovery)

    # Award progress
    ProgressionService.award_discovery(db, current_user.id, req.category, req.conservation_status)

    return {
        "id": discovery.id,
        "name": species.common_name or species.scientific_name,
        "scientificName": species.scientific_name,
        "category": species.category,
        "imageUrl": None,
        "discoveredAt": discovery.discovered_at.isoformat()
    }
