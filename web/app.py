import os

from fastapi import FastAPI
from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)
from starlette import status
from starlette.middleware.base import (
    RequestResponseEndpoint,
    BaseHTTPMiddleware,
)
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from web.api.auth import decode_and_validate_token

import uvicorn

app = FastAPI(debug=True)

app = FastAPI(
    title="Expenses API",
    description="API for managing expenses",
    version="1.0.0",
    openapi_url="/api/v1/expenses/openapi.json",
    docs_url="/api/v1/expenses/docs",
    redoc_url="/api/v1/expenses/redoc",
)


class AuthoriseRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if os.getenv("AUTH_ON", "False") != "True":
            request.state.user_details = "test"
            return await call_next(request)

        if request.url.path in [
            "/expenses/docs",
            "/expenses/openapi.json",
            "/expenses/redoc",
        ]:
            return await call_next(request)

        if request.method == "OPTIONS":
            return await call_next(request)

        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Missing access token",
                    "body": "Missing access token",
                },
            )

        try:
            auth_token = bearer_token.split(" ")[1].strip()
            token_payload = decode_and_validate_token(auth_token)
        except (
            InvalidSignatureError,
            ExpiredSignatureError,
            ImmatureSignatureError,
            InvalidAudienceError,
            MissingRequiredClaimError,
            InvalidKeyError,
            InvalidAlgorithmError,
            InvalidTokenError,
        ) as e:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": str(e), "body": str(e)},
            )
        else:
            request.state.user_details = token_payload["sub"]
        return await call_next(request)


app.add_middleware(AuthoriseRequestMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


from web.api.api import app as api

app.include_router(api, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
