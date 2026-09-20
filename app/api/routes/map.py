from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import SessionDep, get_current_user
from app.models.domain import User
from app.services.map_service import MapService
from app.schemas.map import MapDiscoveryResponse, NearbySpeciesResponse

router = APIRouter()

@router.get("/discoveries", response_model=List[MapDiscoveryResponse])
def get_user_discoveries(
    db: SessionDep,
    current_user: User = Depends(get_current_user)
):
    discoveries = MapService.get_user_discoveries(db, current_user.id)
    return [
        {
            "id": d.id,
            "species_id": d.species_id,
            "species_name": d.species.common_name or d.species.scientific_name,
            "location_lat": d.location_lat,
            "location_lng": d.location_lng,
            "discovered_at": d.discovered_at.isoformat() if d.discovered_at else ""
        }
        for d in discoveries
    ]

@router.get("/species/{species_id}", response_model=List[MapDiscoveryResponse])
def get_species_distribution(
    species_id: int,
    db: SessionDep
):
    discoveries = MapService.get_species_distribution(db, species_id)
    return [
        {
            "id": d.id,
            "species_id": d.species_id,
            "species_name": d.species.common_name or d.species.scientific_name,
            "location_lat": d.location_lat,
            "location_lng": d.location_lng,
            "discovered_at": d.discovered_at.isoformat() if d.discovered_at else ""
        }
        for d in discoveries
    ]

@router.get("/nearby", response_model=List[NearbySpeciesResponse])
def get_nearby_species(
    db: SessionDep,
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius: float = Query(50.0, description="Radius in km")
):
    nearby = MapService.get_nearby_species(db, lat, lng, radius)
    return nearby
