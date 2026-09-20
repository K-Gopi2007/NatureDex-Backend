from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import Optional, List
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    profile_picture: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    total_discoveries: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    discoveries: Mapped[List["Discovery"]] = relationship(back_populates="user")
    collections: Mapped[List["Collection"]] = relationship(back_populates="user")
    scans: Mapped[List["ScanHistory"]] = relationship(back_populates="user")
    achievements: Mapped[List["UserProgress"]] = relationship(back_populates="user")

class Achievement(Base):
    __tablename__ = "achievements"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(String)
    icon: Mapped[str] = mapped_column(String)
    # E.g. "discover_total", "discover_category"
    requirement_type: Mapped[str] = mapped_column(String) 
    requirement_value: Mapped[int] = mapped_column(Integer)
    # E.g. "Bird", "Plant"
    requirement_target: Mapped[Optional[str]] = mapped_column(String, nullable=True) 

class UserProgress(Base):
    __tablename__ = "user_progress"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievements.id"))
    unlocked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="achievements")
    achievement: Mapped["Achievement"] = relationship()

class Reward(Base):
    __tablename__ = "rewards"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    reward_type: Mapped[str] = mapped_column(String) # 'title', 'badge'
    required_level: Mapped[int] = mapped_column(Integer)
    icon: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class Species(Base):
    __tablename__ = "species"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    common_name: Mapped[str] = mapped_column(String, index=True)
    scientific_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    category: Mapped[str] = mapped_column(String, index=True)
    taxonomy: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    habitat: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    distribution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    conservation_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    diet: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    size: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    lifespan: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    discoveries: Mapped[List["Discovery"]] = relationship(back_populates="species")
    scans: Mapped[List["ScanHistory"]] = relationship(back_populates="species")
    collections: Mapped[List["Collection"]] = relationship(back_populates="species")

class Collection(Base):
    __tablename__ = "collections"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    species_id: Mapped[int] = mapped_column(ForeignKey("species.id"))
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="collections")
    species: Mapped["Species"] = relationship(back_populates="collections")

class Discovery(Base):
    __tablename__ = "discoveries"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    species_id: Mapped[int] = mapped_column(ForeignKey("species.id"))
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    location_lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    location_lng: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    user: Mapped["User"] = relationship(back_populates="discoveries")
    species: Mapped["Species"] = relationship(back_populates="discoveries")

class ScanHistory(Base):
    __tablename__ = "scan_history"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    species_id: Mapped[Optional[int]] = mapped_column(ForeignKey("species.id"), nullable=True)
    scanned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    user: Mapped["User"] = relationship(back_populates="scans")
    species: Mapped[Optional["Species"]] = relationship(back_populates="scans")

class CommunityContribution(Base):
    __tablename__ = "community_contributions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    species_id: Mapped[Optional[int]] = mapped_column(ForeignKey("species.id"), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    location_lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    location_lng: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    observation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending") # pending, approved, rejected
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    reviewed_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    reviewer: Mapped[Optional["User"]] = relationship("User", foreign_keys=[reviewed_by])
    species: Mapped[Optional["Species"]] = relationship("Species")
