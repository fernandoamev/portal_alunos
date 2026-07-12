from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
import threading

DATABASE_URL = "sqlite:///./sql_app.db"

# A specific thread-local for holding the database engine connection
# This ensures that each thread gets its own engine if needed, though for SQLite
# with check_same_thread=False, it might not be strictly necessary for the engine itself,
# but it's good practice for managing thread-specific resources.
_thread_local = threading.local()

def get_engine() -> Engine:
    """
    Retrieves or creates the SQLAlchemy engine for the SQLite database.
    Ensures that the engine is created once per process (or thread if specifically configured to be thread-local,
    but `check_same_thread=False` typically means one engine for all threads is fine).
    Using a thread-local for `engine` ensures that if different threads *were* to need different engine configurations
    or connection pools, they would get them. For this simple SQLite case, it's mostly about
    thread-safety for session management.
    """
    if not hasattr(_thread_local, "engine"):
        # For SQLite, `check_same_thread=False` is crucial to allow multiple threads
        # to interact with the same database connection.
        _thread_local.engine = create_engine(
            DATABASE_URL, connect_args={"check_same_thread": False}, future=True
        )
    return _thread_local.engine

# Each instance of the SessionLocal class will be a database session.
# The class itself is not a session, but a "factory" for new session objects.
# We'll use this class in a `with` statement in our code.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine(), future=True)

# We will inherit from this class to create each of the database models or classes (the ORM models).
Base = declarative_base()

def init_db():
    """
    Initializes the database by creating all tables defined in Base.metadata.
    This function should be called at application startup.
    """
    Base.metadata.create_all(bind=get_engine())
