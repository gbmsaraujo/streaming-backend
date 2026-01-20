from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.server.routes.videos_route import video_router

app = FastAPI(debug=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(video_router)
