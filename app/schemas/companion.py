from pydantic import BaseModel
from typing import Optional

class CompanionRequest(BaseModel):
    question: str
    species_context: Optional[str] = None

class CompanionResponse(BaseModel):
    answer: str

class CelebrationRequest(BaseModel):
    species_name: str
