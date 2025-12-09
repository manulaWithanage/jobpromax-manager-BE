from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.config import settings
from app.auth import verify_token
from app.routes import tasks, roadmap, features, dashboard, users

app = FastAPI(title="JobProMax Progress Hub API")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_db():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to JobProMax Progress Hub API"}

# Include Routers
# Include Routers
app.include_router(users.router, prefix="/users", tags=["Users"]) # Auth handled internally
app.include_router(tasks.router, tags=["Tasks"], dependencies=[Depends(verify_token)])
app.include_router(roadmap.router, tags=["Roadmap"], dependencies=[Depends(verify_token)])
app.include_router(features.router, tags=["Features"], dependencies=[Depends(verify_token)])
app.include_router(dashboard.router, tags=["Dashboard"], dependencies=[Depends(verify_token)])
