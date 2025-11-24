from pydantic import BaseModel, Field
from typing import Optional, List
from .quiz import QuizCreate, QuizOut, QuizUpdate
class VideoCreate(BaseModel):
    title: str = Field(...,)
    subtitle: Optional[str] = Field(None,)
    description: Optional[str] = Field(None,)
    url: str = Field(...,)
    quizzes: List[QuizCreate]
    
class VideoOut(BaseModel):
    id: int
    title: str
    subtitle: str
    description: str
    url: str
    quizzes: List[QuizOut]
    
    class Config:
        from_attributes = True
class VideoUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    quizzes: Optional[List[QuizUpdate]] = None
    
    class Config:
        # orm_mode = True #old way pydantic v1
        from_attributes = True #new way pydantic v2