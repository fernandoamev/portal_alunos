from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class StudentBase(BaseModel):
    """
    Base Pydantic schema for Student, containing common attributes.
    """
    name: str = Field(..., min_length=2, max_length=100, description="Nome completo do aluno")
    email: EmailStr = Field(..., description="Endereço de e-mail único do aluno")
    enrollment_number: str = Field(..., min_length=5, max_length=20, description="Número de matrícula único do aluno")
    age: int = Field(..., gt=5, description="Idade do aluno (deve ser maior que 5)")

    class Config:
        from_attributes = True # Or from_orm = True for older Pydantic versions

class StudentCreate(StudentBase):
    """
    Pydantic schema for creating a new Student.
    Inherits from StudentBase and can add specific validation rules for creation.
    """
    # No additional fields or specific validations needed beyond StudentBase for now,
    # but this schema exists for clear separation if needed later.
    pass

class StudentUpdate(BaseModel):
    """
    Pydantic schema for updating an existing Student.
    All fields are optional, allowing for partial updates (PATCH requests).
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Nome completo do aluno")
    email: Optional[EmailStr] = Field(None, description="Endereço de e-mail único do aluno")
    enrollment_number: Optional[str] = Field(None, min_length=5, max_length=20, description="Número de matrícula único do aluno")
    age: Optional[int] = Field(None, gt=5, description="Idade do aluno (deve ser maior que 5)")

    class Config:
        from_attributes = True

class StudentResponse(StudentBase):
    """
    Pydantic schema for responding with Student data.
    Includes database-generated fields like id and created_at.
    """
    id: int = Field(..., description="ID único do aluno no banco de dados")
    created_at: datetime = Field(..., description="Timestamp de criação do registro do aluno")

    class Config:
        from_attributes = True
