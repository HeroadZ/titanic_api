from pydantic import BaseModel
from enum import Enum

class Sex(str, Enum):
    male = "male"
    female = "female"

class Embarked(str, Enum):
    S = "S"
    C = "C"
    Q = "Q"

class PassengerData(BaseModel):
    Name: str | None
    Ticket: str | None
    Cabin: str | None
    Pclass: int
    Sex: Sex
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: Embarked

    class Config:
        use_enum_values = True  # Serialize enums as their values
