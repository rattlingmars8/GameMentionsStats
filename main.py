from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from api import router as api_router
from src.config import settings

app = FastAPI(docs_url=None, redoc_url=None)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_prefix.value)
app.mount("/static", StaticFiles(directory="./client/dist", html=True), name="static")


@app.get("/{full_path:path}")
def serve_react(full_path: str):
    file_path = f"./client/dist/{full_path}"
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse("./client/dist/index.html")


# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Game Mentions Tracker API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
