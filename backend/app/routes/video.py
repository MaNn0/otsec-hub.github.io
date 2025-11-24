from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.video import VideoCreate, VideoOut, VideoUpdate
from app.models.video import Video
from app.models.quiz import Quiz
from app.database import get_db
from typing import List
from dotenv import load_dotenv
from app.routes.announcements import add_announcement
from sqlalchemy import asc
from app.schemas.pagination import PaginatedResponse

load_dotenv()
router = APIRouter()

@router.post("/add_video", response_model=VideoOut)
def add_video(video: VideoCreate, db: Session = Depends(get_db)):
    try:
        # Prepare quiz objects from input
        quiz_objects = [
            Quiz(
                question=q.question,
                option1=q.options[0],
                option2=q.options[1],
                option3=q.options[2],
                option4=q.options[3],
                correct_answer=q.correct_answer
            )
            for q in video.quizzes
        ]

        # Create video with related quizzes
        db_video = Video(
            title=video.title,
            subtitle=video.subtitle,
            description=video.description,
            url=video.url,
            quizzes=quiz_objects
        )
        
        db.add(db_video)
        db.flush()
        
        add_announcement(
            db=db,
            content_type="video",
            content_id=db_video.id,
            title=db_video.title,
            image=db_video.url
        )

        db.commit()
        db.refresh(db_video)
        return db_video

    except IntegrityError as e:
        db.rollback()
        if 'ix_videos_url' in str(e.orig):
            raise HTTPException(status_code=400, detail="Video URL already exists.")
        raise HTTPException(status_code=400, detail="Database integrity error.")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/get_videos", response_model=PaginatedResponse[VideoOut])
async def get_videos(
    page: int = Query(1, ge=1),
    limit: int = Query(9, ge=1),
    db: Session = Depends(get_db),
):
    # Order videos by id ascending
    videos_query = db.query(Video).order_by(asc(Video.id))
    total = videos_query.count()

    videos = videos_query.offset((page - 1) * limit).limit(limit).all()

    # Convert SQLAlchemy objects to Pydantic schemas using from_orm
    video_items = [VideoOut.from_orm(v) for v in videos]

    if not video_items and total > 0 and page > 1:
        raise HTTPException(status_code=404, detail="Page not found")
    elif not video_items and total == 0:
        pass  # Will return empty list

    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        items=video_items
    )


@router.get("/get_video/{video_id}", response_model=VideoOut)
def get_video(video_id: int, db: Session = Depends(get_db)):
    db_video = db.query(Video).filter(Video.id == video_id).first()
    
    if not db_video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return db_video

@router.put("/update_video/{video_id}", response_model=VideoOut)
def update_video(video_id: int, video: VideoUpdate, db: Session = Depends(get_db)):
    db_video = db.query(Video).filter(Video.id == video_id).first()

    if not db_video:
        raise HTTPException(status_code=404, detail="Video not found")

    # Update video fields
    if video.title:
        db_video.title = video.title
    if video.subtitle:
        db_video.subtitle = video.subtitle
    if video.description:
        db_video.description = video.description
    if video.url:
        db_video.url = video.url

    # Update quizzes if provided
    if video.quizzes:
        for updated_quiz in video.quizzes:
            db_quiz = db.query(Quiz).filter(Quiz.id == updated_quiz.id).first()
            if db_quiz:
                if updated_quiz.question:
                    db_quiz.question = updated_quiz.question
                if updated_quiz.correct_answer:
                    db_quiz.correct_answer = updated_quiz.correct_answer
                if updated_quiz.options:
                    db_quiz.option1 = updated_quiz.options[0]
                    db_quiz.option2 = updated_quiz.options[1]
                    db_quiz.option3 = updated_quiz.options[2]
                    db_quiz.option4 = updated_quiz.options[3]

    db.commit()
    db.refresh(db_video)
    return db_video

@router.delete("/delete_video/{video_id}", response_model=VideoOut)
def delete_video(video_id:int,db : Session = Depends(get_db)):
    
    db_video= db.query(Video).filter(Video.id == video_id).first()
    
    if not db_video:
        raise HTTPException(status=404, detail="Video not found")
    
    db.delete(db_video)
    db.commit()
    return JSONResponse(content={"message": "Video deleted successfully"})


# ====================================================================================
# ====================================================================================
# ====================================================================================

