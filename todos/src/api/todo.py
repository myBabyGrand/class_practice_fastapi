from typing import List

from database.connection import get_db
from database.orm import ToDo
from database.repository import ToDoRepository
from fastapi import Depends, HTTPException, Body, APIRouter
from schema.request import CreateTodoRequest
from schema.response import ToDoListSchema, ToDoSchema
from sqlalchemy.orm import Session

router = APIRouter(prefix="/todos")

@router.get("", status_code=200)
def get_todos_handler(
    order: str | None = None,
    todo_repo: ToDoRepository = Depends(ToDoRepository),
) -> ToDoListSchema:
    todos: List[ToDo] = todo_repo.get_todos()

    if order and order == "DESC":
        return ToDoListSchema(
            todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )


@router.get("/{todo_id}", status_code=200)
def get_todo_handler(
    todo_id : int,
    todo_repo: ToDoRepository = Depends(),
) -> ToDoSchema:
    todo: Todo | None = todo_repo.get_todo_by_todo_id(todo_id = todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


@router.post("", status_code=201)
def create_todo_handler(
    request: CreateTodoRequest,
    todo_repo: ToDoRepository = Depends(),
):
    todo: ToDo = ToDo.create(request=request) #pydantic to orm
    todo: ToDo = todo_repo.create_todo(todo=todo) #db save, id generation
    return ToDoSchema.from_orm(todo)


@router.patch("/{todo_id}", status_code=200)
def update_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    todo_repo: ToDoRepository = Depends(),
):
    todo: Todo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)

    if todo:
        todo.done() if is_done else todo.undone()
        todo: ToDo = todo_repo.update_todo(todo=todo)
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


@router.delete("/{todo_id}", status_code=204)
def delete_todo_handler(
    todo_id: int,
    todo_repo: ToDoRepository = Depends(),
):
    todo: Todo | None =  todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")

    todo_repo.delete_todo(todo_id = todo_id)
