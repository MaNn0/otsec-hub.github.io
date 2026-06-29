from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.ExerciseSubmission import ExerciseSubmission
from app.schemas.exerciseSubmission import ExerciseSubmissionCreate, ExerciseSubmissionOut, ExerciseSubmissionUpdate
from app.auth.auth import get_current_user
from app.models.user import User
from fastapi import HTTPException
from typing import List

router = APIRouter()

@router.post("/submit_exercise/{exercise_id}")
def submit_exercise(
    exercise_id: int,
    submission: ExerciseSubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submission_record = ExerciseSubmission(
        exercise_id=exercise_id,
        user_id=current_user.id,
        answers=submission.answers,
        status=submission.status
    )
    db.add(submission_record)
    db.commit()
    db.refresh(submission_record)
    return {"message": "Submission successful"}

@router.get("/submission", response_model=List[ExerciseSubmissionOut])
def get_submission(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    submission = db.query(ExerciseSubmission).options(joinedload(ExerciseSubmission.exercise)).all()
    return submission

@router.patch("/submission/{submission_id}", response_model=ExerciseSubmissionOut)
def update_submission_status(
    submission_id: int,
    update_data: ExerciseSubmissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Optional: check if current_user is allowed to update
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Not authorized")

    submission = db.query(ExerciseSubmission).filter_by(id=submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    submission.status = update_data.status
    db.commit()
    db.refresh(submission)
    return submission