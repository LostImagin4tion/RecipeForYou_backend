from typing import List, Optional, Union

from fastapi import Depends
from database.repositories.ingredient_repository import IngredientRepository, IngredientDB


class IngredientService:
    ingredient_repository: IngredientRepository

    def __init__(
            self,
            ingredient_repository: IngredientRepository = Depends()
    ) -> None:
        self.ingredient_repository = ingredient_repository

    async def create(self, ingredient: IngredientDB) -> Union[IngredientDB, List[IngredientDB], None]:
        return await self.ingredient_repository.add(ingredient)

    async def delete(self, ingredient: IngredientDB) -> Optional[IngredientDB]:
        return await self.ingredient_repository.delete(ingredient)

    async def get_all(self) -> List[Optional[IngredientDB]]:
        return await self.ingredient_repository.get_all()

    async def get(self, ingredient: IngredientDB) -> Optional[IngredientDB]:
        return await self.ingredient_repository.get_one(ingredient)

    async def update(
            self,
            request_ingredient: IngredientDB,
            new_ingredient: IngredientDB
    ) -> Optional[IngredientDB]:
        return await self.ingredient_repository.update(request_ingredient, new_ingredient)
