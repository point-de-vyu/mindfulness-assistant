from fastapi import HTTPException
from fastapi import status


def raise_400_error(msg: str = "Invalid parameter") -> None:
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
    )


def raise_401_error(msg: str = "Invalid token") -> None:
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=msg
    )


def raise_404_error(msg: str = "Not found") -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=msg
    )