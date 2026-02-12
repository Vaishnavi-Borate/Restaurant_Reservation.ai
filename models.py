from pydantic import BaseModel

class Reservation(BaseModel):
    name: str
    phone: str
    date: str
    time: str
    people: int

class Waitlist(BaseModel):
    name: str
    phone: str
    phone: str
    people: int
