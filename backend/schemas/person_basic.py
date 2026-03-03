from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum


class RoleEnum(str, Enum):
    member_basic = "member_basic"
    member_close = "member_close"
    co_operator = "co_operator"
    admin = "admin"

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"    

class PersonBasicCreate(BaseModel):
    sur_name: Optional[str] = ""
    last_name: str
    middle_name: Optional[str] = ""
    first_name: str
    gender: GenderEnum
    birth_date: Optional[date] = None
    death_date: Optional[date] = None
    avatar: Optional[str] = None
    role: RoleEnum

class PersonBasicUpdate(BaseModel):
    sur_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None    
    first_name: Optional[str] = None
    gender: Optional[GenderEnum] = None
    birth_date: Optional[date] = None
    death_date: Optional[date] = None
    avatar: Optional[str] = None

class RestoreRequest(BaseModel):
    role: RoleEnum