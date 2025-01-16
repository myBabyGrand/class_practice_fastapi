from http import HTTPStatus

from database.repository import UserRepository
from schema.request import SignUpRequest, LogInRequest, CreateOTPRequest, VerifyOTPRequest
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from schema.response import UserSchema, JWTResponse
from service.user import UserService
from database.orm import User
from cache import redis_client
from security import get_access_token

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

@router.post("/email/otp", status_code=HTTPStatus.CREATED)
def create_otp_handler(
        request: CreateOTPRequest,
        _: str = Depends(get_access_token),
        user_service: UserService = Depends()
):
    # 1. access_token이 있어야 하고(사용은 안함)
    # 2. request body에 email 주소 받음
    # 3. otp create
    otp_value: int = user_service.create_otp()
    # 4. redis에 저장 (key = email주소, value = otp값)
    redis_client.set(request.email_address, otp_value)
    redis_client.expire(request.email_address, 3*60)
    # 5. send otp to email

    return {"otp" : otp_value}


@router.post("/email/otp/verify")
def verify_otp_handler(
        request: VerifyOTPRequest,
        backgroud_task:BackgroundTasks,
        access_token: str = Depends(get_access_token),
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends()
):
    # 1. access_token이 있어야 하고
    # 2. request body에 email 주소, otp 받음
    # 3. verify otp value
    validOtp: str | None = redis_client.get(request.email_address)
    if not validOtp:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Bad Request")

    if request.otp != int(validOtp):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Bad Request")

    username = user_service.decode_jwt(access_token=access_token)
    by_username : User = user_repo.get_user_by_username(username)
    if not by_username :
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User Not Found")
    # 4. user.email update -- 일단 구현하지 않음
    # 5. email 알림

    backgroud_task.add_task(
        user_service.send_email_to_user,
        request.email_address
    )

    return UserSchema.from_orm(by_username)