from datetime import datetime
import secrets
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker, Session

from settings import DATABASE

URL = "{engine}://{username}:{password}@{host}:{port}/{database}".format(
    **DATABASE)
engine = create_engine(URL)

session_factory = sessionmaker(bind=engine)
db: Session = scoped_session(session_factory)


Model = declarative_base()


class Link(Model):
    __tablename__ = "links"

    id = Column(String(10), primary_key=True)
    destination = Column(String(1024), unique=True)
    created = Column(DateTime)

    def __init__(self, destination) -> None:
        self.id = secrets.token_urlsafe(6)

        self.destination = destination
        self.created = datetime.now()


Model.metadata.create_all(engine)
