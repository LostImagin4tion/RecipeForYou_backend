from typing import List, Optional, Union

from fastapi import Depends
from database.repositories.recipe_repository import RecipeRepository, RecipeDB


class RecipeService:
    recipe_repository: RecipeRepository

    def __init__(
            self,
            recipe_repository: RecipeRepository = Depends()
    ) -> None:
        self.recipe_repository = recipe_repository

    async def get_all(self) -> List[Optional[RecipeDB]]:
        return await self.recipe_repository.get_all()

    async def get(self, recipe: RecipeDB) -> Optional[RecipeDB]:
        return await self.recipe_repository.get_one(recipe)

    async def get_ingredients(self, recipe: RecipeDB) -> Optional[RecipeDB]:
        return (await self.recipe_repository.get_one(recipe)).ingredients

    async def add(self, recipe: RecipeDB) -> Union[RecipeDB, List[RecipeDB], None]:
        return await self.recipe_repository.add(recipe)

    async def update(
            self,
            request_recipe: RecipeDB,
            new_recipe: RecipeDB
    ) -> Optional[RecipeDB]:
        return await self.recipe_repository.update(request_recipe, new_recipe)

    async def delete(self, recipe: RecipeDB) -> Optional[RecipeDB]:
        return await self.recipe_repository.delete(recipe)
