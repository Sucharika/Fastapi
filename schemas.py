from __future__ import annotations
from typing import Optional, List, Union

from passlib.context import CryptContext
from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR

pwd_context = CryptContext(schemes=["bcrypt"])


class UserOutput(SQLModel):
    id: int
    username: str


class User(SQLModel, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
    password_hash: str = ""

    def set_password(self, password):
        """Setting the passwords actually sets password_hash."""
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        """Verify given password by hashing and comparing to password_hash."""
        return pwd_context.verify(password, self.password_hash)


class TripInput(SQLModel):
    start: int
    end: int
    description: str


class TripOutput(TripInput):
    id: int


class Trip(TripInput, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    car_id: int = Field(foreign_key="car.id")
    car: Car = Relationship(back_populates="trips")


class CarInput(SQLModel):
    size: str
    fuel: Optional[str] = None,
    doors: int
    transmission: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "size": "m",
                "doors": 5,
                "transmission": "auto",
                "fuel": "hybrid"
            }
        }


class Car(CarInput, table=True):
    id: Union[int, None] = Field(primary_key=True, default=None)
    trips: list[Trip] = Relationship(back_populates="car")


class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []


