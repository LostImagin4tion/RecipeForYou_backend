from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status

from api.schemas.token_schema import TokenSchema
from api.services.token_service import TokenService
from database.repositories.token_repository import TokenDB

tokenRouter = APIRouter(
    prefix="/v1/tokens", tags=["token"]
)


@tokenRouter.get("/", response_model=List[TokenSchema])
async def index(
    name: Optional[str] = None,
    page_size: Optional[int] = 100,
    start_index: Optional[int] = 0,
    token_service: TokenService = Depends(),
):
    return [
        token.normalize()
        for token in await token_service.get_all()
    ]


@tokenRouter.get('/{id}', response_model=TokenSchema)
async def get(
        uid: UUID,
        token_service: TokenService = Depends()
):
    return (await token_service.get(TokenDB(uid))).normalize()


@tokenRouter.patch(
    '/{id}',
    response_model=TokenSchema,
    status_code=status.HTTP_404_NOT_FOUND
)
async def update(
    uid: int,
    new_token: TokenDB,
    token_service: TokenService = Depends(),
):
    return (
        await token_service.update(
            request_token=TokenDB(uid),
            new_token=new_token
        )
    ).normalize()


@tokenRouter.delete(
    '/{id}',
    status_code=status.HTTP_404_NOT_FOUND
)
async def delete(
        uid: int,
        token_service: TokenService = Depends()
):
    return (await token_service.delete(TokenDB(uid))).normalize()
