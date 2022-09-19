from typing import Union
from uuid import UUID

from pydantic import BaseModel


class TokenSchema(BaseModel):
    uid: Union[UUID, str, None]
    is_active: Union[bool, str, None]
    user_email: Union[str, None]
