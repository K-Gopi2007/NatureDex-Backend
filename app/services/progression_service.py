from sqlalchemy.orm import Session
from app.models.domain import User, Achievement, UserProgress, Reward, Discovery
from datetime import datetime, timezone
from typing import List, Dict, Any

class ProgressionService:
    XP_PER_DISCOVERY = 100
    XP_PER_ACHIEVEMENT = 200

    @staticmethod
    def calculate_level(xp: int) -> int:
        return (xp // 500) + 1

    @staticmethod
    def seed_achievements(db: Session):
        default_achievements = [
            {"name": "First Discovery", "description": "Make your first discovery.", "icon": "🌟", "requirement_type": "discover_total", "requirement_value": 1},
            {"name": "10 Discoveries", "description": "Discover 10 species.", "icon": "🏆", "requirement_type": "discover_total", "requirement_value": 10},
            {"name": "Bird Expert", "description": "Discover 3 birds.", "icon": "🦅", "requirement_type": "discover_category", "requirement_value": 3, "requirement_target": "bird"},
            {"name": "Plant Expert", "description": "Discover 3 plants.", "icon": "🌿", "requirement_type": "discover_category", "requirement_value": 3, "requirement_target": "plant"},
            {"name": "Conservation Hero", "description": "Discover an endangered species.", "icon": "🛡️", "requirement_type": "discover_endangered", "requirement_value": 1},
        ]
        
        for ach in default_achievements:
            existing = db.query(Achievement).filter(Achievement.name == ach["name"]).first()
            if not existing:
                new_ach = Achievement(**ach)
                db.add(new_ach)
        
        db.commit()

    @staticmethod
    def award_discovery(db: Session, user_id: int, species_category: str = "", conservation_status: str = "") -> Dict[str, Any]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {}

        user.total_discoveries += 1
        user.xp += ProgressionService.XP_PER_DISCOVERY

        # Fetch achievements to evaluate
        achievements = db.query(Achievement).all()
        user_progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
        unlocked_ids = {up.achievement_id for up in user_progress}

        newly_unlocked = []

        # We can't do complex historical queries here easily without full Discovery records, 
        # but we can rely on total_discoveries for total, and approximate for categories if we had full history.
        # Let's count discoveries per category
        discoveries = db.query(Discovery).filter(Discovery.user_id == user_id).all()
        
        cat_counts = {}
        for d in discoveries:
            cat = (d.species.category or "").lower()
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
        
        # Add current one if not already flushed
        curr_cat = (species_category or "").lower()
        cat_counts[curr_cat] = cat_counts.get(curr_cat, 0) + 1

        for ach in achievements:
            if ach.id in unlocked_ids:
                continue
            
            unlocked = False
            if ach.requirement_type == "discover_total":
                if user.total_discoveries >= ach.requirement_value:
                    unlocked = True
            elif ach.requirement_type == "discover_category":
                target = ach.requirement_target.lower() if ach.requirement_target else ""
                # Substring match (e.g. "bird" in "Bird of Prey")
                count = sum(v for k, v in cat_counts.items() if target in k)
                if count >= ach.requirement_value:
                    unlocked = True
            elif ach.requirement_type == "discover_endangered":
                status = (conservation_status or "").lower()
                if "endangered" in status or "threatened" in status:
                    unlocked = True

            if unlocked:
                up = UserProgress(user_id=user_id, achievement_id=ach.id)
                db.add(up)
                user.xp += ProgressionService.XP_PER_ACHIEVEMENT
                newly_unlocked.append({
                    "id": ach.id,
                    "title": ach.name,
                    "description": ach.description,
                    "icon": ach.icon
                })
        
        old_level = user.level
        user.level = ProgressionService.calculate_level(user.xp)

        db.commit()

        return {
            "xp_added": ProgressionService.XP_PER_DISCOVERY + (len(newly_unlocked) * ProgressionService.XP_PER_ACHIEVEMENT),
            "new_total_xp": user.xp,
            "new_level": user.level,
            "leveled_up": user.level > old_level,
            "new_achievements": newly_unlocked
        }

    @staticmethod
    def get_user_progress(db: Session, user_id: int) -> Dict[str, Any]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {}
        
        progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
        achievements = []
        for p in progress:
            achievements.append({
                "id": p.achievement.id,
                "title": p.achievement.name,
                "description": p.achievement.description,
                "icon": p.achievement.icon,
                "unlockedAt": p.unlocked_at.isoformat() if p.unlocked_at else None
            })
            
        rank = "Novice Explorer"
        if user.level >= 5: rank = "Journeyman Explorer"
        if user.level >= 10: rank = "Master Explorer"
        if user.level >= 20: rank = "Grandmaster Explorer"
        
        return {
            "xp": user.xp,
            "level": user.level,
            "total_discoveries": user.total_discoveries,
            "rank": rank,
            "achievements": achievements
        }
