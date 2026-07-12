from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

# Importações dos módulos da aplicação
from src.app.database import init_db
from src.app.routes.student_routes import student_router

app = FastAPI(
    title="Student Management API",
    description="API para gerenciamento de estudantes em uma universidade fictícia.",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    """
    Função para inicializar o banco de dados na inicialização da aplicação.
    """
    await init_db()
    print("Database initialized and connected.")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Manipulador de exceção global para HTTPExceptions.
    Retorna uma resposta JSON com o status code e o detalhe da exceção.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# Registro dos routers
app.include_router(student_router, prefix="/students", tags=["students"])

# Exemplo de rota raiz
@app.get("/", status_code=status.HTTP_200_OK, tags=["root"])
async def root():
    return {"message": "Welcome to the Student Management API!"}
