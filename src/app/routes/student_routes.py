from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.app.database import SessionLocal, get_engine
from src.app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from src.app.services.student_service import StudentService
from src.app.exceptions import StudentAlreadyExistsError, StudentNotFoundError
from src.app.models.student import Base # Import Base to ensure tables are created

# Create all tables in the database (for initial setup)
Base.metadata.create_all(bind=get_engine())

router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student_route(student: StudentCreate, db: Session = Depends(get_db)):
    """
    Cria um novo estudante no sistema.
    Retorna o estudante criado com seu ID e timestamp.
    """
    try:
        return StudentService.create_student(db, student)
    except StudentAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/", response_model=List[StudentResponse])
def list_students_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todos os estudantes com suporte a paginação.
    """
    return StudentService.list_students(db, skip=skip, limit=limit)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student_by_id_route(student_id: int, db: Session = Depends(get_db)):
    """
    Obtém os detalhes de um estudante específico pelo seu ID.
    """
    try:
        return StudentService.get_student_by_id(db, student_id)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{student_id}", response_model=StudentResponse)
def update_student_route(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    """
    Atualiza as informações de um estudante existente.
    """
    try:
        return StudentService.update_student(db, student_id, student)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except StudentAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_route(student_id: int, db: Session = Depends(get_db)):
    """
    Deleta um estudante do sistema pelo seu ID.
    """
    try:
        StudentService.delete_student(db, student_id)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
