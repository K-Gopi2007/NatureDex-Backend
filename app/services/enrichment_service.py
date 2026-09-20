import logging
import httpx
from typing import Dict, Any, Optional
import urllib.parse

logger = logging.getLogger(__name__)

class EnrichmentService:
    @staticmethod
    async def get_gbif_data(scientific_name: str) -> Dict[str, Any]:
        """Fetch taxonomy, habitat, distribution and conservation status from GBIF"""
        result = {
            "taxonomy": None,
            "conservation_status": None,
            "habitat": None,
            "distribution": None
        }
        
        try:
            encoded_name = urllib.parse.quote(scientific_name)
            url = f"https://api.gbif.org/v1/species/match?name={encoded_name}"
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("matchType") != "NONE":
                        taxonomy = {}
                        for rank in ["kingdom", "phylum", "class", "order", "family", "genus", "species"]:
                            if rank in data:
                                taxonomy[rank.capitalize()] = data[rank]
                        
                        result["taxonomy"] = taxonomy if taxonomy else None
                        result["conservation_status"] = data.get("status", "Unknown").capitalize()
                        
                        usage_key = data.get("usageKey")
                        if usage_key:
                            # Fetch speciesProfiles for habitat
                            profiles_res = await client.get(f"https://api.gbif.org/v1/species/{usage_key}/speciesProfiles")
                            if profiles_res.status_code == 200:
                                profiles = profiles_res.json().get("results", [])
                                habitats = [p.get("habitat").capitalize() for p in profiles if p.get("habitat")]
                                if habitats:
                                    result["habitat"] = ", ".join(list(set(habitats)))
                            
                            # Fetch distributions
                            dist_res = await client.get(f"https://api.gbif.org/v1/species/{usage_key}/distributions")
                            if dist_res.status_code == 200:
                                dists = dist_res.json().get("results", [])
                                locations = [d.get("locality") or d.get("country") for d in dists]
                                locations = [loc for loc in locations if loc]
                                if locations:
                                    result["distribution"] = ", ".join(list(set(locations))[:5]) # Top 5 locations
        except Exception as e:
            logger.warning(f"GBIF enrichment failed for {scientific_name}: {e}")
        
        return result

    @staticmethod
    async def get_wikipedia_data(name: str) -> Dict[str, Any]:
        """Fetch description from Wikipedia"""
        try:
            encoded_name = urllib.parse.quote(name.replace(" ", "_"))
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_name}"
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    extract = data.get("extract")
                    return {"description": extract}
        except Exception as e:
            logger.warning(f"Wikipedia enrichment failed for {name}: {e}")
            
        return {"description": None}

    @staticmethod
    async def enrich_species(scientific_name: str, common_name: str) -> Dict[str, Any]:
        """Combine data from multiple sources"""
        gbif_data = await EnrichmentService.get_gbif_data(scientific_name)
        wiki_data = await EnrichmentService.get_wikipedia_data(scientific_name)
        
        if not wiki_data.get("description") and common_name:
            wiki_data = await EnrichmentService.get_wikipedia_data(common_name)
            
        return {
            "taxonomy": gbif_data.get("taxonomy"),
            "conservation_status": gbif_data.get("conservation_status"),
            "description": wiki_data.get("description"),
            "habitat": gbif_data.get("habitat"),
            "distribution": gbif_data.get("distribution")
        }
