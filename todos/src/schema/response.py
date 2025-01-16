from typing import List
from pydantic import BaseModel

class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    #from orm
    class Config:
        orm_mode = True

class ToDoListSchema(BaseModel):
    todos: List[ToDoSchema]

class UserSchema(BaseModel):
    id: int
    username: str

    #from orm
    class Config:
        orm_mode = True

class JWTResponse(BaseModel):
    access_token: str