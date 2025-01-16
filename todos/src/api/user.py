from http import HTTPStatus

from database.repository import UserRepository
from schema.request import SignUpRequest, LogInRequest
from fastapi import APIRouter, Depends, HTTPException
from schema.response import UserSchema, JWTResponse
from service.user import UserService
from database.orm import User

router = APIRouter(prefix="/users")


@router.post("/sign-up", status_code=HTTPStatus.CREATED)
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends()
    ):
    # 1. request body(username, password)
    # 2. password -> hasing -> hashed_password
    hashed_password: str = user_service.hash_password(
        plain_password=request.password
    )
    # 3. User(username, hashed_password)
    user: User = User.create(
        username=request.username,
        hashed_password=hashed_password
    )
    # 4. user -> Db save
    saved_user: User = user_repo.save_user(user=user)

    # 5. return user(id, username)
    return UserSchema.from_orm(saved_user)

@router.post("/log-in", status_code=HTTPStatus.CREATED)
def user_log_in_handler(
        request: LogInRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends()
):
    #1. request body(username, password)
    #2. db read user
    selected_user: User | None = user_repo.get_user_by_username(username=request.username)
    if not selected_user:
        raise HTTPException(status_code = HTTPStatus.NOT_FOUND, detail = "User Not Found")

    #3. user.password, request.password -> bycrypt.checkpw
    verified: bool = user_service.verify_password(
        plain_password=request.password,
        hashed_password=selected_user.password
    )

    # 4. invalid user
    if not verified:
        raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED, detail = "Not Authorized")

    #5. valid user : create & return jwt
    access_token: str = user_service.create_jwt(username=selected_user.username)
    return JWTResponse(access_token = access_token)