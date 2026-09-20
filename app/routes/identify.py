from fastapi import APIRouter, File, UploadFile, HTTPException
from app.schemas.identify import IdentifyResult
from app.services.identify_service import IdentifyService

router = APIRouter()

@router.post("/", response_model=IdentifyResult)
async def identify_species(image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    
    try:
        content = await image.read()
        mime_type = image.content_type
        result = await IdentifyService.identify_image(content, mime_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
