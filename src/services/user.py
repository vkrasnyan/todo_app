from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import user_crud
from models.user import User
from schemas.user import UserCreate, UserCreateDB, UserLogin
from utilities.security.password_hasher import (
    get_password_hash,
    verify_password,
)
from utilities.security.security import TokenSubject, create_tokens


async def create(db: AsyncSession, create_schema: UserCreate) -> User:
    if exsisted_username := await user_crud.get_by_username(
        db=db, username=create_schema.username
    ):
        raise Exception(
            f"Username {exsisted_username.username} already exsists!"
        )

    if create_schema.password != create_schema.password_confirm:
        raise Exception("Passwords don't match!")
    del create_schema.password_confirm
    create_schema.password = get_password_hash(create_schema.password)
    create_data = UserCreateDB(**create_schema.model_dump(exclude_unset=True))
    return await user_crud.create(db=db, create_schema=create_data)


async def login(db_obj: User, login_data: UserLogin) -> dict:
    if verify_password(
        plain_password=login_data.password,
        hashed_password=db_obj.password,
    ):
        subject = TokenSubject(
            username=str(db_obj.username),
            password=db_obj.password,
        )
        return await create_tokens(subject)
    raise Exception("Wrong username or password!")
