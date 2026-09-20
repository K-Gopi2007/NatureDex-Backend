from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from datetime import datetime, timezone

from app.api.deps import get_db, get_current_user
from app.models.domain import User, CommunityContribution
from app.schemas.contribution import ContributionCreate, ContributionResponse, AdminReview

router = APIRouter()

@router.post("/", response_model=ContributionResponse)
def submit_contribution(
    contribution_in: ContributionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contribution = CommunityContribution(
        user_id=current_user.id,
        species_id=contribution_in.species_id,
        image_url=contribution_in.image_url,
        location_lat=contribution_in.location_lat,
        location_lng=contribution_in.location_lng,
        observation_notes=contribution_in.observation_notes,
        status="pending"
    )
    db.add(contribution)
    db.commit()
    db.refresh(contribution)
    return contribution

@router.get("/pending", response_model=List[ContributionResponse])
def get_pending_contributions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized. Admins only.")
        
    stmt = select(CommunityContribution).where(CommunityContribution.status == "pending")
    contributions = db.scalars(stmt).all()
    return contributions

@router.post("/{contribution_id}/review", response_model=ContributionResponse)
def review_contribution(
    contribution_id: int,
    review_in: AdminReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized. Admins only.")
        
    contribution = db.get(CommunityContribution, contribution_id)
    if not contribution:
        raise HTTPException(status_code=404, detail="Contribution not found.")
        
    if review_in.status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Status must be approved or rejected.")
        
    contribution.status = review_in.status
    contribution.reviewed_at = datetime.now(timezone.utc)
    contribution.reviewed_by = current_user.id
    
    # If approved, this theoretically becomes "Community Data" 
    # (e.g. used for Maps, or enriching Species records)
    
    db.commit()
    db.refresh(contribution)
    return contribution

@router.get("/me", response_model=List[ContributionResponse])
def get_my_contributions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(CommunityContribution).where(CommunityContribution.user_id == current_user.id)
    contributions = db.scalars(stmt).all()
    return contributions
