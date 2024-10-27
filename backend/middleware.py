from fastapi import HTTPException, Request, status
from functools import wraps


def Auth(header_name: str = "X-Token"):
    def decorator(func):
        print('printed data')
        @wraps(func)
        async def wrapper(*args, **kwargs):
            print('enter')
            print(args)
            print(kwargs)
            token = kwargs['request'].headers.get(header_name)
            token = "expected_token"
            if token != "expected_token":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Forbidden: Invalid or missing token",
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator