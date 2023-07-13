from fastapi import FastAPI

from src.api.routers import candidates, projects

app = FastAPI()

app.include_router(candidates.router, prefix="/candidates", tags=["candidates"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
