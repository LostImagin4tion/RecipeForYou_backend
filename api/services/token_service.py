from typing import List, Optional, Union

from fastapi import Depends
from database.repositories.token_repository import TokenRepository, TokenDB


class TokenService:
    token_repository: TokenRepository

    def __init__(
            self,
            token_repository: TokenRepository = Depends()
    ) -> None:
        self.token_repository = token_repository

    async def create(self, token: TokenDB) -> Union[TokenDB, List[TokenDB], None]:
        return await self.token_repository.add(token)

    async def delete(self, token: TokenDB) -> Optional[TokenDB]:
        return await self.token_repository.delete(token)

    async def get_all(self) -> List[Optional[TokenDB]]:
        return await self.token_repository.get_all()

    async def get(self, token: TokenDB) -> Optional[TokenDB]:
        return await self.token_repository.get_one(token)

    async def update(
            self,
            request_token: TokenDB,
            new_token: TokenDB
    ) -> Optional[TokenDB]:
        return await self.token_repository.update(request_token, new_token)
