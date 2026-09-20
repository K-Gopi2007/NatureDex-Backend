from fastapi import APIRouter, Depends
from app.api.deps import CurrentUser, SessionDep
from app.schemas.user import UserResponse
from app.services.progression_service import ProgressionService
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: CurrentUser):
    return current_user

@router.get("/me/progress")
def get_user_progress(db: SessionDep, current_user: CurrentUser):
    return ProgressionService.get_user_progress(db, current_user.id)

class AwardRequest(BaseModel):
    species_category: Optional[str] = ""
    conservation_status: Optional[str] = ""

@router.post("/me/progress/award")
def award_discovery_progress(
    request: AwardRequest,
    db: SessionDep,
    current_user: CurrentUser
):
    return ProgressionService.award_discovery(
        db, 
        current_user.id, 
        request.species_category, 
        request.conservation_status
    )

