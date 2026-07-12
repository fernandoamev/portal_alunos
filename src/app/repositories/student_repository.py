from typing import List, Optional
from sqlalchemy.orm import Session
from src.app.models.student import Student

class StudentRepository:
    """
    Repository class for Student model.
    Handles all database access logic related to students.
    """

    @staticmethod
    def save(db: Session, student: Student) -> Student:
        """
        Saves a new student or updates an existing one in the database.
        """
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    @staticmethod
    def get_by_id(db: Session, student_id: int) -> Optional[Student]:
        """
        Retrieves a student by their unique ID.
        """
        return db.query(Student).filter(Student.id == student_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[Student]:
        """
        Retrieves a student by their email address.
        """
        return db.query(Student).filter(Student.email == email).first()

    @staticmethod
    def get_by_enrollment(db: Session, enrollment: str) -> Optional[Student]:
        """
        Retrieves a student by their enrollment number.
        """
        return db.query(Student).filter(Student.enrollment_number == enrollment).first()

    @staticmethod
    def list_all(db: Session, skip: int = 0, limit: int = 100) -> List[Student]:
        """
        Lists all students with pagination.
        """
        return db.query(Student).offset(skip).limit(limit).all()

    @staticmethod
    def delete(db: Session, student_id: int) -> bool:
        """
        Deletes a student by their unique ID.
        Returns True if the student was deleted, False otherwise.
        """
        student = db.query(Student).filter(Student.id == student_id).first()
        if student:
            db.delete(student)
            db.commit()
            return True
        return False
