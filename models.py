from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base, engine


class Urls(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    random = Column(String, nullable=False, unique=True)


if __name__ == "__main__":
    Base.metadata.create_all(engine)


