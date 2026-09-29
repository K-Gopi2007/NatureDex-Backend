from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from app.schemas.identify import IdentifyResult
from app.services.identify_service import IdentifyService
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=IdentifyResult)
@limiter.limit("5/minute")
async def identify_species(request: Request, image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    
    try:
        content = await image.read()
        if len(content) > 5 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 5MB.")
            
        mime_type = image.content_type
        result = await IdentifyService.identify_image(content, mime_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to identify species: {str(e)}")
