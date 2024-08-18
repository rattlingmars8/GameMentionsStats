from fastapi import FastAPI

from api import router as api_router
from src.config import settings

app = FastAPI()
app.include_router(api_router, prefix=settings.api_prefix.value)


@app.get("/")
async def root():
    return {"message": "Welcome to the Game Mentions Tracker API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
