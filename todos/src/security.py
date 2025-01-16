from http import HTTPStatus

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException

def get_access_token(
        auto_header: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False))
    ) -> str:
    if auto_header is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Not Authorized")

    return auto_header.credentials