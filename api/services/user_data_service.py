from typing import List, Optional, Union

from fastapi import Depends
from database.repositories.user_data_repository import UserDataRepository, UserDataDB


class UserDataService:
    user_data_repository: UserDataRepository

    def __init__(
            self,
            user_data_repository: UserDataRepository = Depends()
    ) -> None:
        self.user_data_repository = user_data_repository

    async def create(self, user_data: UserDataDB) -> Union[UserDataDB, List[UserDataDB], None]:
        return await self.user_data_repository.add(user_data)

    async def delete(self, user_data: UserDataDB) -> Optional[UserDataDB]:
        return await self.user_data_repository.delete(user_data)

    async def get_all(self) -> List[Optional[UserDataDB]]:
        return await self.user_data_repository.get_all()

    async def get(self, user_data: UserDataDB) -> Optional[UserDataDB]:
        return await self.user_data_repository.get_one(user_data)

    async def update(
            self,
            request_user_data: UserDataDB,
            new_user_data: UserDataDB
    ) -> Optional[UserDataDB]:
        return await self.user_data_repository.update(request_user_data, new_user_data)
