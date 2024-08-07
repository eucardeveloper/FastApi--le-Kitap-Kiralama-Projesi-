from fastapi import Request, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from app.models import User


api_keys = {}
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def get_api_key(api_key_header: str = Security(api_key_header),) -> str:

    if api_key_header in api_keys.keys():

        return api_key_header

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


def get_operation_user(r: Request) -> User:
    apikey = r.headers.get("x-api-key")
    return api_keys[apikey]


def require_admin(r: Request) -> User:

    operation_user = get_operation_user(r)

    if operation_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access",
        )

    return operation_user


def require_customer(r: Request) -> User:

    operation_user = get_operation_user(r)

    if operation_user["role"] != "customer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access",
        )

    return operation_user

def require_authenticated(r: Request) -> User:

    operation_user = get_operation_user(r)

    if operation_user["role"] != "admin" and operation_user["role"] != "customer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access",
        )

    return operation_user