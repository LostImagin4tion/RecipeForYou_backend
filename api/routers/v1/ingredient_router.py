from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status

from api.schemas.ingredient_schema import IngredientSchema
from api.services.ingredient_service import IngredientService
from database.repositories.ingredient_repository import IngredientDB

IngredientRouter = APIRouter(
    prefix="/v1/ingredients", tags=["Ingredient"]
)


@IngredientRouter.get("/", response_model=List[IngredientSchema])
async def index(
    name: Optional[str] = None,
    page_size: Optional[int] = 100,
    start_index: Optional[int] = 0,
    ingredient_service: IngredientService = Depends(),
):
    return [
        ingredient.normalize()
        for ingredient in await ingredient_service.get_all()
    ]


@IngredientRouter.get('/{id}', response_model=IngredientSchema)
async def get(
        uid: UUID,
        ingredient_service: IngredientService = Depends()
):
    return (await ingredient_service.get(IngredientDB(uid))).normalize()


@IngredientRouter.patch(
    '/{id}',
    response_model=IngredientSchema,
    status_code=status.HTTP_404_NOT_FOUND
)
async def update(
    uid: int,
    new_ingredient: IngredientDB,
    ingredient_service: IngredientService = Depends(),
):
    return (
        await ingredient_service.update(
            request_ingredient=IngredientDB(uid),
            new_ingredient=new_ingredient
        )
    ).normalize()


@IngredientRouter.delete(
    '/{id}',
    status_code=status.HTTP_404_NOT_FOUND
)
async def delete(
        uid: int,
        ingredient_service: IngredientService = Depends()
):
    return (await ingredient_service.delete(IngredientDB(uid))).normalize()
