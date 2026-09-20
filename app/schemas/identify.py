from pydantic import BaseModel, Field
from typing import Optional, Dict, List

class SecondarySpecies(BaseModel):
    common_name: str = Field(description="The common name of the secondary species")
    scientific_name: str = Field(description="The scientific name of the secondary species")
    category: str = Field(description="The category of the secondary species")
    confidence: float = Field(description="Confidence score for this secondary species (0.0 to 1.0)")


class IdentifyResult(BaseModel):
    common_name: str = Field(description="The common name of the species")
    scientific_name: str = Field(description="The scientific name of the species")
    category: str = Field(description="The category of the species, e.g. Plant, Animal, Insect, Bird, Fungi, etc.")
    confidence: float = Field(description="The confidence score of the identification, between 0 and 1")
    
    # Enrichment fields
    taxonomy: Optional[Dict[str, str]] = Field(default=None, description="Taxonomic hierarchy")
    habitat: Optional[str] = Field(default=None, description="Typical habitat")
    distribution: Optional[str] = Field(default=None, description="Geographic distribution")
    description: Optional[str] = Field(default=None, description="Detailed description")
    conservation_status: Optional[str] = Field(default=None, description="Conservation status")
    diet: Optional[str] = Field(default=None, description="Typical diet or feeding habits")
    size: Optional[str] = Field(default=None, description="Average size or weight")
    lifespan: Optional[str] = Field(default=None, description="Average lifespan")
    
    secondary_species: Optional[List[SecondarySpecies]] = Field(default=[], description="Any other species detected in the background or alongside the primary species. Useful for images with multiple species.")
