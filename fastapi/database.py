from sqlmodel import create_engine, Session
import os

sqlite_url = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database.db')}"
engine = create_engine(sqlite_url, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
