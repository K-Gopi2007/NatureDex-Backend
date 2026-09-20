import logging
import json
from google import genai
from google.genai import types
from app.schemas.identify import IdentifyResult
from app.core.config import settings

logger = logging.getLogger(__name__)

class IdentifyService:
    @staticmethod
    async def identify_image(image_bytes: bytes, mime_type: str) -> IdentifyResult:
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "YOUR_API_KEY_HERE":
            logger.error("GEMINI_API_KEY is not set or is using placeholder.")
            raise ValueError("Gemini API key is not configured.")

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        try:
            logger.info(f"Sending image to Gemini Vision (size: {len(image_bytes)} bytes, type: {mime_type})")
            
            response = await client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                    "Identify the biological species in this image. The image may be blurry, partial, or contain multiple species. Try your best to identify the primary subject even if conditions are poor. Provide its common name, scientific name, category (e.g. Plant, Animal, Fungi, Insect, Bird), and a confidence score between 0.0 and 1.0. Also provide typical diet, size, lifespan, habitat, distribution, and conservation status if known. If you detect other distinct species in the background or alongside the primary subject, list them in the 'secondary_species' array."
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=IdentifyResult,
                    temperature=0.2,
                )
            )
            
            logger.info("Received response from Gemini Vision.")
            
            if not response.text:
                 raise ValueError("Empty response from Gemini API")
                 
            data = json.loads(response.text)
            
            # Enrich the result
            try:
                from app.services.enrichment_service import EnrichmentService
                enrichment = await EnrichmentService.enrich_species(
                    data.get("scientific_name", ""),
                    data.get("common_name", "")
                )
                
                # Merge enrichment data (only keys that are populated)
                for k, v in enrichment.items():
                    if v is not None:
                        data[k] = v
            except Exception as enrich_err:
                logger.warning(f"Failed to enrich species data: {enrich_err}")

            # Validate response via pydantic model
            result = IdentifyResult(**data)
            return result
            
        except Exception as e:
            logger.error(f"Error during Gemini Vision identification: {str(e)}")
            raise ValueError(f"Identification failed: {str(e)}")
