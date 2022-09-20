from typing import Union
from uuid import UUID

from pydantic import BaseModel


class RecipeSchema(BaseModel):
    uid: Union[UUID, str, None]
    name: str

