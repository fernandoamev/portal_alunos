from typing import List, Optional
from sqlalchemy.orm import Session

from src.app.models.student import Student
from src.app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from src.app.repositories.student_repository import StudentRepository
from src.app.exceptions import StudentAlreadyExistsError, StudentNotFoundError

class StudentService:
    """
    Service layer for managing student-related business logic.
    Handles validations and interactions with the StudentRepository.
    """

    @staticmethod
    def create_student(db: Session, student_data: StudentCreate) -> StudentResponse:
        """
        Creates a new student after performing business validations.
        - Prevents creation if email or enrollment number already exists.
        """
        if StudentRepository.get_by_email(db, student_data.email):
            raise StudentAlreadyExistsError(f"Student with email '{student_data.email}' already exists.")
        if StudentRepository.get_by_enrollment(db, student_data.enrollment_number):
            raise StudentAlreadyExistsError(f"Student with enrollment number '{student_data.enrollment_number}' already exists.")

        db_student = Student(**student_data.model_dump())
        db_student = StudentRepository.save(db, db_student)
        return StudentResponse.model_validate(db_student)

    @staticmethod
    def get_student_by_id(db: Session, student_id: int) -> StudentResponse:
        """
        Retrieves a student by their ID.
        Raises StudentNotFoundError if the student does not exist.
        """
        student = StudentRepository.get_by_id(db, student_id)
        if not student:
            raise StudentNotFoundError(f"Student with ID '{student_id}' not found.")
        return StudentResponse.model_validate(student)

    @staticmethod
    def list_students(db: Session, skip: int = 0, limit: int = 100) -> List[StudentResponse]:
        """
        Lists students with pagination.
        """
        students = StudentRepository.list_all(db, skip, limit)
        return [StudentResponse.model_validate(student) for student in students]

    @staticmethod
    def update_student(db: Session, student_id: int, student_data: StudentUpdate) -> StudentResponse:
        """
        Updates an existing student's information.
        - Raises StudentNotFoundError if the student does not exist.
        - Prevents update if new email or enrollment number already exists for another student.
        """
        db_student = StudentRepository.get_by_id(db, student_id)
        if not db_student:
            raise StudentNotFoundError(f"Student with ID '{student_id}' not found.")

        update_data = student_data.model_dump(exclude_unset=True)

        if 'email' in update_data and update_data['email'] != db_student.email:
            if StudentRepository.get_by_email(db, update_data['email']):
                raise StudentAlreadyExistsError(f"Email '{update_data['email']}' already in use by another student.")

        if 'enrollment_number' in update_data and update_data['enrollment_number'] != db_student.enrollment_number:
            if StudentRepository.get_by_enrollment(db, update_data['enrollment_number']):
                raise StudentAlreadyExistsError(f"Enrollment number '{update_data['enrollment_number']}' already in use by another student.")

        for key, value in update_data.items():
            setattr(db_student, key, value)

        db_student = StudentRepository.save(db, db_student)
        return StudentResponse.model_validate(db_student)

    @staticmethod
    def delete_student(db: Session, student_id: int) -> None:
        """
        Deletes a student by their ID.
        Raises StudentNotFoundError if the student does not exist.
        """
        if not StudentRepository.delete(db, student_id):
            raise StudentNotFoundError(f"Student with ID '{student_id}' not found.")
