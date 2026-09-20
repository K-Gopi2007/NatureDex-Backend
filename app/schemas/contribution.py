from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContributionCreate(BaseModel):
    species_id: Optional[int] = None
    image_url: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    observation_notes: Optional[str] = None

class ContributionResponse(BaseModel):
    id: int
    user_id: int
    species_id: Optional[int]
    image_url: Optional[str]
    location_lat: Optional[float]
    location_lng: Optional[float]
    observation_notes: Optional[str]
    status: str
    submitted_at: datetime
    reviewed_at: Optional[datetime]
    reviewed_by: Optional[int]

    class Config:
        from_attributes = True

class AdminReview(BaseModel):
    status: str # 'approved' or 'rejected'
