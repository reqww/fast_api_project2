from fastapi import APIRouter

from microblog import blog

routers = APIRouter()
routers.include_router(blog.router, prefix='/blog')