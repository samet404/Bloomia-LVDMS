from datetime import date

from pydantic import BaseModel, ConfigDict, ValidationError


class Event(BaseModel):
    name: str

event = Event(name="Test Event")
print(event.model_dump())
print(event.model_dump_json())
print(event.model_dump_json(indent=4))

class Event(BaseModel):
    name: str
    date: date
    config: ConfigDict = ConfigDict(validate_assignment=True)