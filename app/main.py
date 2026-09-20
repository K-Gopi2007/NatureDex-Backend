import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import species, discoveries, auth, users, map, companion
from app.routes import identify
from app.core.config import settings
from app.db.database import SessionLocal
from app.services.progression_service import ProgressionService
from app.services.seeder_service import SeederService

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        ProgressionService.seed_achievements(db)
        SeederService.seed_species(db)
    finally:
        db.close()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(species.router, prefix=f"{settings.API_V1_STR}/species", tags=["species"])
app.include_router(discoveries.router, prefix=f"{settings.API_V1_STR}/discoveries", tags=["discoveries"])
app.include_router(map.router, prefix=f"{settings.API_V1_STR}/map", tags=["map"])
app.include_router(companion.router, prefix=f"{settings.API_V1_STR}/companion", tags=["companion"])
app.include_router(identify.router, prefix=f"{settings.API_V1_STR}/identify", tags=["identify"])
from app.api.routes import contributions
app.include_router(contributions.router, prefix=f"{settings.API_V1_STR}/contributions", tags=["contributions"])

@app.get("/")
def root():
    return {"message": "Welcome to NatureDex AI API"}
