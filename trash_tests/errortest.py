import json

from pydantic import BaseModel

from src.helpers import safe_parse_pydantic_model


class Person(BaseModel):
    name: str
    age: int
    email: str


person = safe_parse_pydantic_model(Person, json.loads('{"name": "John", "age": "30", "email": "john@example.com"}'))
print(person)