from fastapi import FastAPI
from starlette.responses import Response
from starlette.requests import Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

from core.db import SessionLocal
from routers import routers
from user.logic import user_db, SECRET
from user.schemes import User, UserCreate, UserDB, UserUpdate

app = FastAPI()

auth_backends = []
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)
auth_backends.append(jwt_authentication)

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends, 
    User, 
    UserCreate, 
    UserUpdate,
    UserDB,
)

@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")

def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")

app.include_router(routers)
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(on_after_register),
    prefix="/auth", 
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(), 
    prefix="/users", 
    tags=["users"]
)
