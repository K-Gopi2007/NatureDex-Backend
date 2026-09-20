from sqlalchemy.orm import Session
from app.models.domain import Discovery, Species
from typing import List, Optional

class MapService:
    @staticmethod
    def get_user_discoveries(db: Session, user_id: int) -> List[Discovery]:
        return db.query(Discovery).filter(
            Discovery.user_id == user_id,
            Discovery.location_lat.isnot(None),
            Discovery.location_lng.isnot(None)
        ).all()

    @staticmethod
    def get_species_distribution(db: Session, species_id: int) -> List[Discovery]:
        # Represents all recorded discoveries of this species globally
        return db.query(Discovery).filter(
            Discovery.species_id == species_id,
            Discovery.location_lat.isnot(None),
            Discovery.location_lng.isnot(None)
        ).all()

    @staticmethod
    def get_nearby_species(db: Session, lat: float, lng: float, radius_km: float = 50.0) -> List[dict]:
        # Basic bounding box approach for nearby species (1 degree ~ 111km)
        lat_diff = radius_km / 111.0
        lng_diff = radius_km / 111.0  # Rough approximation, ignore cosine of latitude for simplicity here
        
        discoveries = db.query(Discovery).filter(
            Discovery.location_lat.between(lat - lat_diff, lat + lat_diff),
            Discovery.location_lng.between(lng - lng_diff, lng + lng_diff)
        ).all()
        
        # Group by species and return unique species with one of their locations
        species_map = {}
        for d in discoveries:
            if d.species_id not in species_map:
                species_map[d.species_id] = {
                    "species_id": d.species_id,
                    "species_name": d.species.common_name or d.species.scientific_name,
                    "location_lat": d.location_lat,
                    "location_lng": d.location_lng
                }
        
        return list(species_map.values())
