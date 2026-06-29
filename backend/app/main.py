from fastapi import FastAPI
from app.routes import user, auth, educators, video, userProgress, pieProgress, lab, exercise, exerciseSubmission, communityLab, communityVideo, analytics, announcements
from app import models

from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

origins = [os.getenv("REACT_DOT_SERVER").strip(),
    "http://localhost:3000"] #Allow Localhost for development

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(user.router, tags=["users"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(educators.router, prefix="/api", tags=["educators"])
app.include_router(video.router, prefix="/api", tags=["videos"])
app.include_router(userProgress.router, prefix="/api", tags=["video_views"])
app.include_router(lab.router, prefix="/api", tags=["labs"])
app.include_router(announcements.router, prefix="/api", tags=["announcements"])
app.include_router(communityLab.router, prefix="/api", tags=["communityLab"])
app.include_router(communityVideo.router, prefix="/api", tags=["communityVideo"])
app.include_router(exercise.router, prefix="/api", tags=["exercisess"])
app.include_router(pieProgress.router, prefix="/api/progress", tags=["pieProgress"])
app.include_router(exerciseSubmission.router, prefix="/api", tags=["exerciseSubmission"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])


# Initialize database
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)