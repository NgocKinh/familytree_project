from sqlalchemy.orm import Session
from sqlalchemy import or_
from .models import Person


def get_children(db: Session, source_id: int):
    """
    Trả về danh sách con ruột trực tiếp của source.
    Không recursive.
    """
    return db.query(Person).filter(
        or_(
            Person.father_id == source_id,
            Person.mother_id == source_id
        )
    ).all()
