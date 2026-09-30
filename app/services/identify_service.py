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
            import base64
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")

            interaction = await client.aio.interactions.create(
                model=getattr(settings, 'GEMINI_MODEL', 'gemini-3.8-flash'),
                input=[
                    {
                        "type": "image",
                        "mime_type": mime_type,
                        "data": image_b64,
                    },
                    {
                        "type": "text",
                        "text": "Identify the biological species in this image. The image may be blurry, partial, or contain multiple species. Try your best to identify the primary subject even if conditions are poor. Provide its common name, scientific name, category (e.g. Plant, Animal, Fungi, Insect, Bird), and a confidence score between 0.0 and 1.0. Also provide typical diet, size, lifespan, habitat, distribution, and conservation status if known. If you detect other distinct species in the background or alongside the primary subject, list them in the 'secondary_species' array. Output ONLY valid JSON matching the requested fields."
                    }
                ],
                response_format=[
                    {
                        "type": "text",
                        "mime_type": "application/json",
                        "schema": IdentifyResult.model_json_schema(),
                    }
                ]
            )
            
            logger.info("Received response from Gemini Vision.")
            
            if not interaction.output_text:
                 raise ValueError("Empty response from Gemini API")
                 
            data = json.loads(interaction.output_text)
            
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
