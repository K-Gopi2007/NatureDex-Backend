from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_discoveries():
    return {"message": "List of discoveries"}

@router.post("/")
def create_discovery():
    return {"message": "Discovery created"}
