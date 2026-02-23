from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from .models import Person, Spouse


def get_current_spouses(db: Session, person_id: int):
    """
    Trả về danh sách spouse hợp lệ cho Affinity.
    Hợp lệ khi status != 'divorced'
    """

    return (
        db.query(Person)
        .join(
            Spouse,
            or_(
                and_(
                    Spouse.person1_id == person_id,
                    Spouse.person2_id == Person.id,
                ),
                and_(
                    Spouse.person2_id == person_id,
                    Spouse.person1_id == Person.id,
                ),
            ),
        )
        .filter(Spouse.status != "divorced")
        .all()
    )
