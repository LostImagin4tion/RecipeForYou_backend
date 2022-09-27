from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status

from api.schemas.user_data_schema import UserDataSchema
from api.services.user_data_service import UserDataService
from database.repositories.user_data_repository import UserDataDB

UserDataRouter = APIRouter(
    prefix="/v1/user_datas", tags=["user_data"]
)


@UserDataRouter.get("/", response_model=List[UserDataSchema])
async def index(
    name: Optional[str] = None,
    page_size: Optional[int] = 100,
    start_index: Optional[int] = 0,
    user_data_service: UserDataService = Depends(),
):
    return [
        user_data.normalize()
        for user_data in await user_data_service.get_all()
    ]


@UserDataRouter.get('/{id}', response_model=UserDataSchema)
async def get(
        uid: UUID,
        user_data_service: UserDataService = Depends()
):
    return (await user_data_service.get(UserDataDB(uid))).normalize()


@UserDataRouter.patch(
    '/{id}',
    response_model=UserDataSchema,
    status_code=status.HTTP_404_NOT_FOUND
)
async def update(
    uid: int,
    new_user_data: UserDataDB,
    user_data_service: UserDataService = Depends(),
):
    return (
        await user_data_service.update(
            request_user_data=UserDataDB(uid),
            new_user_data=new_user_data
        )
    ).normalize()


@UserDataRouter.delete(
    '/{id}',
    status_code=status.HTTP_404_NOT_FOUND
)
async def delete(
        uid: int,
        user_data_service: UserDataService = Depends()
):
    return (await user_data_service.delete(UserDataDB(uid))).normalize()
