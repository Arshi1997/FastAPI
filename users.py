from pydantic import BaseModel

class user(BaseModel):
    id: int
    name: str
    age: int
    std: str
    gender: str