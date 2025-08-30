from fastapi import FastAPI

from src.api.routers.auth import router as auth_router
from src.api.routers.resumes import router as resumes_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(resumes_router)

@app.get('/')
async def test():
    return {'status': 'ok'}
