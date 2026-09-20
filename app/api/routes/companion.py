from fastapi import APIRouter, HTTPException, Depends
from app.schemas.companion import CompanionRequest, CompanionResponse, CelebrationRequest
from app.services.companion_service import CompanionService
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/ask", response_model=CompanionResponse)
async def ask_companion(
    request: CompanionRequest,
    current_user = Depends(get_current_user)
):
    try:
        answer = await CompanionService.ask_question(request.question, request.species_context)
        return CompanionResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/celebrate", response_model=CompanionResponse)
async def celebrate_discovery(
    request: CelebrationRequest,
    current_user = Depends(get_current_user)
):
    try:
        answer = await CompanionService.generate_celebration(request.species_name)
        return CompanionResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
