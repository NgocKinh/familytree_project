from enum import Enum

class EdgeType(str, Enum):
    BLOOD_PARENT = "BLOOD_PARENT"
    BLOOD_CHILD = "BLOOD_CHILD"
    MARRIAGE = "MARRIAGE"
    LEGAL = "LEGAL"   # adoption / guardian (chuẩn bị cho tương lai)