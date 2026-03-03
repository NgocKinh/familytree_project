from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class MarriageCreate(BaseModel):
    spouse_a_id: int = Field(..., example=1)
    spouse_b_id: int = Field(..., example=2)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    ceremony_type: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    consanguineous: Optional[int] = 0