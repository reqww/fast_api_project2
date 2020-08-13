from fastapi_users.db import SQLAlchemyUserDatabase

from .models import User
from .schemes import UserDB
from core.db import SessionLocal

users = User.__table__
user_db = SQLAlchemyUserDatabase(UserDB, SessionLocal, users)

SECRET = 'a;klsjipoasdg98pahgapoidsoipsadpasdghposadihg8pagpnausdioh'