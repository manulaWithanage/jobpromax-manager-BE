from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.config import settings
from app.routes import tasks, roadmap, features, dashboard

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
app.include_router(tasks.router, tags=["Tasks"])
app.include_router(roadmap.router, tags=["Roadmap"])
app.include_router(features.router, tags=["Features"])
app.include_router(dashboard.router, tags=["Dashboard"])
