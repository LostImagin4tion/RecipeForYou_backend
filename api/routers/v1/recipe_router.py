from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status

from api.schemas.recipe_schema import RecipeSchema
from api.services.recipe_service import RecipeService
from database.repositories.recipe_repository import RecipeDB

RecipeRouter = APIRouter(
    prefix="/v1/recipes", tags=["Recipe"]
)


@RecipeRouter.get("/", response_model=List[RecipeSchema])
async def index(
    name: Optional[str] = None,
    page_size: Optional[int] = 100,
    start_index: Optional[int] = 0,
    recipe_service: RecipeService = Depends(),
):
    return [
        recipe.normalize()
        for recipe in await(recipe_service.get_all())
    ]


@RecipeRouter.get('/{id}', response_model=RecipeSchema)
async def get(
        uid: UUID,
        recipe_service: RecipeService = Depends()
):
    return (await recipe_service.get(RecipeDB(uid))).normalize()


@RecipeRouter.patch(
    '/{id}',
    response_model=RecipeSchema,
    status_code=status.HTTP_404_NOT_FOUND
)
async def update(
    uid: int,
    new_recipe: RecipeDB,
    recipe_service: RecipeService = Depends(),
):
    return (
        await recipe_service.update(
            request_recipe=RecipeDB(uid),
            new_recipe=new_recipe
        )
    ).normalize()


@RecipeRouter.delete(
    '/{id}', status_code=status.HTTP_404_NOT_FOUND
)
async def delete(
        uid: int,
        recipe_service: RecipeService = Depends()
):
    return (await recipe_service.delete(RecipeDB(uid))).normalize()


@RecipeRouter.get(
    '/{id}/ingredients/',
    response_model=List[RecipeSchema],
    status_code=status.HTTP_404_NOT_FOUND
)
async def get_ingredients(
        uid: int,
        recipe_service: RecipeService = Depends()
):
    return [
        ingredient.normalize()
        for ingredient in (await recipe_service.get_ingredients(RecipeDB(uid))).ingredients
    ]
