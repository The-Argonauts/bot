from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.Base import Base

DATABASE_URL = "sqlite:///../db.sqlite3"

# Create database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured Session class
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():

    from models import Business, Feedback, TestPlan, User

    # Create tables in the database
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
