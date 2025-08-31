from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.auth import router as auth_router
from src.api.routers.resumes import router as resumes_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(resumes_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
