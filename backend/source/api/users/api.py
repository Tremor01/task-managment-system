from fastapi import APIRouter, Depends

from db.models.user import User
from schemas.user import UserCreate, UserRead, UserUpdate

from .user_manager import auth_backend, current_active_user, fastapi_users



TAGS_AUTH  = ["Auth"]
TAGS_USERS = ["Users"] 

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=TAGS_AUTH
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=TAGS_AUTH,
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=TAGS_AUTH,
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=TAGS_AUTH,
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=TAGS_USERS,
)


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
