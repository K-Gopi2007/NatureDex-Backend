from sqlalchemy.orm import Session
from app.models.domain import Species

class SeederService:
    @staticmethod
    def seed_species(db: Session):
        sample_species = [
            {
                "common_name": "Monarch Butterfly",
                "scientific_name": "Danaus plexippus",
                "category": "Insect",
                "habitat": "Meadows, prairies, and fields",
                "distribution": "North America, South America, Oceania",
                "conservation_status": "Endangered",
                "diet": "Milkweed (larvae), Nectar (adults)",
                "size": "3.5 to 4 inches wingspan",
                "lifespan": "2 to 6 weeks (summer), up to 8 months (winter)"
            },
            {
                "common_name": "Red Panda",
                "scientific_name": "Ailurus fulgens",
                "category": "Animal",
                "habitat": "High-altitude temperate forests with bamboo understories",
                "distribution": "Himalayas, Southwestern China",
                "conservation_status": "Endangered",
                "diet": "Bamboo, fruit, insects",
                "size": "20 to 25 inches (head-body), plus 11 to 19 inches tail",
                "lifespan": "8 to 10 years in the wild, up to 15 years in captivity"
            },
            {
                "common_name": "Blue Jay",
                "scientific_name": "Cyanocitta cristata",
                "category": "Bird",
                "habitat": "Forest edges, woodlands, parks",
                "distribution": "Eastern and Central North America",
                "conservation_status": "Least Concern",
                "diet": "Nuts, seeds, insects, small vertebrates",
                "size": "9 to 12 inches length",
                "lifespan": "7 years in the wild"
            },
            {
                "common_name": "Giant Sequoia",
                "scientific_name": "Sequoiadendron giganteum",
                "category": "Plant",
                "habitat": "Western slopes of the Sierra Nevada mountains",
                "distribution": "California, USA",
                "conservation_status": "Endangered",
                "diet": "Photosynthesis",
                "size": "Up to 250-300 feet tall",
                "lifespan": "Up to 3,000 years"
            }
        ]
        
        for sp in sample_species:
            existing = db.query(Species).filter(Species.scientific_name == sp["scientific_name"]).first()
            if not existing:
                db.add(Species(**sp))
        
        db.commit()
