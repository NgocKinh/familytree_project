from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    father_id = Column(Integer, ForeignKey("person.id"), nullable=True)
    mother_id = Column(Integer, ForeignKey("person.id"), nullable=True)
    name = Column(String, nullable=True)
    avatar_path = Column(String(255), nullable=True)
class Spouse(Base):
    __tablename__ = "spouse"

    id = Column(Integer, primary_key=True, index=True)

    person1_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    person2_id = Column(Integer, ForeignKey("person.id"), nullable=False)

    status = Column(String, nullable=False)
