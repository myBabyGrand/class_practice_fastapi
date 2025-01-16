from datetime import datetime, timedelta

import bcrypt
from jose import jwt

class UserService:
    encoding: str = "UTF-8"
    secretkey: str = "thisIsSecretKey"
    jwr_algorithm: str = "HS256"

    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)

    def verify_password(self, plain_password:str, hashed_password:str) -> bool :
        #TODO : try-catch로 checkpw에서 발생하는 exception을 처리해야함.
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
        )

    def create_jwt(self, username: str) -> str:
        return jwt.encode(
    {
                "sub" : username,
                "exp" : datetime.now() + timedelta(days=1)
           },
           self.secretkey,
           algorithm=self.jwr_algorithm
        )

    def decode_jwt(self, access_token: str):
        payload: dict = jwt.decode(access_token, self.secretkey, algorithms=[self.jwr_algorithm])
        return payload["sub"] #username