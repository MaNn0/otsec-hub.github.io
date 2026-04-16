from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.exercise import Exercise
from fastapi.responses import JSONResponse
from app.routes.announcements import add_announcement
from app.schemas.exercise import ExerciseCreate, ExerciseOut, ExerciseUpdate
from app.auth.auth import get_current_user
from app.models.user import User
from typing import List

router = APIRouter()

@router.post('/create_exercise', response_model=ExerciseOut)
async def create_exercise(
    exercise_data: ExerciseCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    new_exercise = Exercise(
        title=exercise_data.title,
        subtitle=exercise_data.subtitle,
        content=exercise_data.content,
        questions=exercise_data.questions # Assuming questions is a list of strings
    )
    db.add(new_exercise)
    db.flush()
    
    add_announcement(
        db=db,
        content_type="exercise",
        content_id=new_exercise.id,
        title=new_exercise.title,
        image=''
    )
    
    db.commit()
    db.refresh(new_exercise)
    return new_exercise

@router.get('/get_exercises', response_model=List[ExerciseOut])
async def get_exercises(db: Session = Depends(get_db)):
    # Removed , current_user: User = Depends(get_current_user) to make excercises public
    exercises = db.query(Exercise).all()
    if not exercises:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercises

@router.get('/get_exercise/{id}', response_model=ExerciseOut)
async def get_lab(id: int, db: Session = Depends(get_db)):
# Removed , current_user: User = Depends(get_current_user) to make excercises public
    exercise = db.query(Exercise).filter(Exercise.id == id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


@router.put("/update_exercise/{exercise_id}", response_model=ExerciseOut)
def update_lab(exercise_id: int, exercise: ExerciseUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()

    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # Update exercise fields
    if exercise.title:
        db_exercise.title = exercise.title
    if exercise.subtitle:
        db_exercise.subtitle = exercise.subtitle
    if exercise.content:
        db_exercise.content = exercise.content

    if exercise.questions:
        db_exercise.questions = exercise.questions

    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.delete("/delete_exercise/{exercise_id}", status_code=200)
async def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()

    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    db.delete(db_exercise)
    db.commit()
    return JSONResponse(content={"message": "Exercise deleted successfully"})


# @router.post("/user_lab_progress", status_code=201) #check exercise quiz complete 
# async def create_user_progress(
#     progress_data: UserProgressCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     # Check if the record already exists (based on PK constraint)
#     existing_progress = db.query(UserProgress).filter_by(
#         user_id=current_user.id,
#         content_type=progress_data.content_type,
#         content_id=progress_data.content_id
#     ).first()

#     if existing_progress:
#         raise HTTPException(status_code=409, detail="Progress already recorded for this content.")

#     new_progress = UserProgress(
#         user_id=current_user.id,
#         content_type=progress_data.content_type,
#         content_id=progress_data.content_id
#     )
#     db.add(new_progress)
#     db.commit()

#     return Response(status_code=201)

# @router.get('/lab_quiz',)
