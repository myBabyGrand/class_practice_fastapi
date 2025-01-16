from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    # id: int
    contents: str
    is_done: bool


class SignUpRequest(BaseModel):
    username: str
    password: str

class LogInRequest(BaseModel):
    username: str
    password: str


class CreateOTPRequest(BaseModel):
    email_address: str

class VerifyOTPRequest(BaseModel):
    email_address: str
    otp: int