from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.schema import UniqueConstraint

from src.app.database import Base

class Student(Base):
    """
    SQLAlchemy model for a student.
    Represents the 'students' table in the database.
    """
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    enrollment_number = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        UniqueConstraint('email', name='uq_student_email'),
        UniqueConstraint('enrollment_number', name='uq_student_enrollment_number'),
    )

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', email='{self.email}')>"
