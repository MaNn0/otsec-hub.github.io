from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.video import Video
from app.models.lab import Lab
from app.models.exercise import Exercise
from app.models.ExerciseSubmission import ExerciseSubmission
from app.database import get_db

router = APIRouter()

@router.get("/analytics")
def get_overview(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_videos = db.query(Video).count()
    total_labs = db.query(Lab).count()
    total_exercises = db.query(Exercise).count()
    total_submissions = db.query(ExerciseSubmission).count()

    return {
        "users": total_users,
        "videos": total_videos,
        "labs": total_labs,
        "exercises": total_exercises,
        "submissions": total_submissions
    }
