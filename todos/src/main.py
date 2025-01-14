from database.connection import get_db
from fastapi import FastAPI, Body, HTTPException, Depends
from schema.request import CreateTodoRequest
from schema.response import ToDoSchema, ToDoListSchema
from sqlalchemy.orm import Session
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo,delete_todo
from database.orm import ToDo
from typing import List


app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping": "pong"}

todo_data = {
    1:{
        "id": 1,
        "contents": "실전! FastAPI 섹션 1 수강",
        "is_done": True,
    },
    2: {
        "id": 2,
        "contents": "실전! FastAPI 섹션 2 수강",
        "is_done": False,
    },
    3: {
        "id": 3,
        "contents": "실전! FastAPI 섹션 3 수강",
        "is_done": False,
    }
}

# @app.get("/todos")
# def get_todos_handler():
#     return list(todo_data.values())

# @app.get("/todos", status_code=200)
# def get_todos_handler2(order: str | None = None):
#     ret = list(todo_data.values())
#     if order and order == "DESC":
#         return ret[::-1]
#     return ret
#
# @app.get("/todos/{todo_id}", status_code=200)
# def get_todo_handler(todo_id : int):
#     todo= todo_data.get(todo_id)
#     if todo:
#         return todo
#     raise HTTPException(status_code=404, detail="ToDo Not Found")
#
#
# class CreateTodoRequest(BaseModel):
#     id: int
#     contents: str
#     is_done: bool
#
# @app.post("/todos", status_code=201)
# def create_todo_handler(request: CreateTodoRequest):
#     todo_data[request.id] = request.dict()
#     return todo_data[request.id]
#
#
# @app.patch("/todos/{todo_id}", status_code=200)
# def update_todo_handler(
#         todo_id: int,
#         is_done: bool = Body(..., embed=True)
# ):
#     todo = todo_data.get(todo_id)
#     if todo:
#         todo["is_done"] = is_done
#         return todo
#     raise HTTPException(status_code=404, detail="ToDo Not Found")
#
# @app.delete("/todos/{todo_id}", status_code=204)
# def delete_todo_handler(todo_id: int):
#     todo = todo_data.pop(todo_id, None)
#     if todo:
#         return
#     raise HTTPException(status_code=404, detail="ToDo Not Found")

'''N건 조회'''
@app.get("/todos", status_code=200)
def get_todos_handler2(
    order: str | None = None,
    session: Session = Depends(get_db)
) -> ToDoListSchema:
    todos: List[ToDo] = get_todos(session=session)

    if order and order == "DESC":
        return ToDoListSchema(
            todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )

'''단일 조회(by ID)'''
@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
    todo_id : int,
    session: Session = Depends(get_db)
) -> ToDoSchema:
    todo: Todo | None = get_todo_by_todo_id(session=session, todo_id = todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


@app.post("/todos", status_code=201)
def create_todo_handler(
    request: CreateTodoRequest,
    session: Session = Depends(get_db)
):
    todo: ToDo = ToDo.create(request=request) #pydantic to orm
    todo: ToDo = create_todo(session=session, todo=todo) #db save, id generation
    return ToDoSchema.from_orm(todo)


@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    session: Session = Depends(get_db)
):
    todo: Todo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)

    if todo:
        todo.done() if is_done else todo.undone()
        todo: ToDo = update_todo(session=session,todo=todo)
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(
    todo_id: int,
    session: Session = Depends(get_db)
):
    todo: Todo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")

    delete_todo(session=session, todo_id = todo_id)



