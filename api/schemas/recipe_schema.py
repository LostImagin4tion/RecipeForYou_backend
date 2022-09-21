from typing import Union
from uuid import UUID

from pydantic import BaseModel


class RecipeSchema(BaseModel):
    uid: Union[UUID, str, None]
    name: str
    images_name: Union[str, None]
    ingredients: Union[str, None]
    steps: Union[str, None]
    time_required: Union[str, None]
    portions_quantity: Union[str, None]
    difficulty: Union[str, None]
    vegetarian: Union[str, None]
    kitchen: Union[str, None]
    technology: Union[str, None]
    calories: Union[str, None]
    categories: Union[str, None]
    equipment: Union[str, None]

