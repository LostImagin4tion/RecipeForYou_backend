from typing import Union
from uuid import UUID

from pydantic import BaseModel


class UserDataSchema(BaseModel):
    uid: Union[UUID, str, None]
    email: Union[str, None]
    is_admin: Union[bool, str, None]
