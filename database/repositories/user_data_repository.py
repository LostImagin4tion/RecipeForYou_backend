from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.dml import Update
from sqlalchemy.sql.expression import select, delete, update
from uuid import UUID, uuid4
from typing import Optional, List, Union, Any


from database.create_tables import UserDataModel


class UserDataDB:
    __tablename__ = UserDataModel.__tablename__

    uid: Union[UUID, str, None]
    email: Union[str, None]
    is_admin: Union[bool, str, None]

    def __init__(
            self,
            uid='',
            email='',
            is_admin=''
    ):
        self.uid = uid
        self.email = email
        self.is_admin = is_admin

    def __repr__(self):
        return f'<UserDataDB(uid={self.uid}, email={self.email}, is_admin={self.is_admin}'

    __str__ = __repr__

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UserDataDB):
            return False

        return (
            self.uid == other.uid and
            self.email == other.email and
            self.is_admin == other.is_admin
        )

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, UserDataDB):
            return False

        return (
            (self.uid == other.uid or self.uid == '') and
            (self.email == other.email or self.email == '') and
            (self.is_admin == other.is_admin or self.is_admin == '')
        )

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, UserDataDB):
            return False

        return (
            (self.uid == other.uid or self.uid == '') and
            (self.email == other.email or self.email == '') and
            (self.is_admin == other.is_admin or self.is_admin == '')
        )

    def normalize(self) -> dict:
        return {
            "uid": self.uid.__str__(),
            "email": self.email.__str__(),
            "isAdmin": self.is_admin.__str__(),
        }


def fill_query(
        query,
        request_user_data: UserDataDB = '',
        new_user_data: UserDataDB = ''
):
    is_query_empty = True

    if request_user_data != '':

        if request_user_data.uid != '':
            is_query_empty = False
            query = query.where(UserDataModel.uid == request_user_data.uid)

        if request_user_data.email != '':
            is_query_empty = False
            query = query.where(UserDataModel.email == request_user_data.email)

        if request_user_data.is_admin != '':
            is_query_empty = False
            query = query.where(UserDataModel.is_admin == request_user_data.is_admin)

    if isinstance(query, Update):
        if is_query_empty:
            return None
        is_query_empty = True

        if new_user_data != '':

            if request_user_data.email != '':
                is_query_empty = False
                request_user_data.email = new_user_data.email
                query = query.values(email=new_user_data.email)

            if request_user_data.is_admin != '':
                is_query_empty = False
                request_user_data.is_admin = new_user_data.is_admin
                query = query.values(is_admin=new_user_data.is_admin)

    if is_query_empty:
        return None

    return query


class UserDataRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, request_user_data: UserDataDB = '') -> List[Optional[UserDataDB]]:
        query = fill_query(select(UserDataModel), request_user_data)

        user_datas = [
            UserDataDB(
                uid=user_data.uid,
                email=user_data.email,
                is_admin=user_data.is_admin
            ) for user_data in (await self.session.execute(query)).scalars()
        ]

        return user_datas

    async def get_one(self, request_user_data: UserDataDB = '') -> Optional[UserDataDB]:
        user_datas = await self.get_all(request_user_data)

        if user_datas and user_datas[0]:
            return user_datas[0]
        return None

    async def delete(self, request_user_data: UserDataDB = '') -> Optional[UserDataDB]:
        query = fill_query(delete(UserDataDB), request_user_data)

        response_user_data = await self.get_one(request_user_data)
        await self.session.execute(query)
        await self.session.commit()

        return response_user_data

    async def add(
            self,
            request_user_datas: Union[UserDataDB, List[UserDataDB]]
    ) -> Union[UserDataDB, List[UserDataDB], None]:

        if isinstance(request_user_datas, UserDataDB):
            request_user_datas = [request_user_datas]

        for user_data in request_user_datas:
            params = {}

            if user_data.uid != '':
                if isinstance(user_data.uid, str):
                    try:
                        params['uid'] = UUID(user_data.uid)
                    except ValueError:
                        raise ValueError(f'Unable to add new user_data'
                                         f'because parameter "uid" is incorrect')

                elif isinstance(user_data.uid, UUID):
                    params['uid'] = user_data.uid

                else:
                    params['uid'] = uuid4()

            if user_data.email != '':
                params['email'] = user_data.email
            else:
                raise ValueError(f'Unable to add new user_data'
                                 f'because parameter "email" does not exist')

            if user_data.is_admin != '':
                params['is_admin'] = user_data.is_admin
            else:
                raise ValueError(f'Unable to add new user_data'
                                 f'because parameter "is_admin" does not exist')

            self.session.add(UserDataModel(**params))

        await self.session.commit()

        response_user_data = []
        for user_data in request_user_datas:
            response_user_data.append(await self.get_one(user_data))

        if len(response_user_data) == 1:
            response_user_data = response_user_data[0]
        elif not len(response_user_data):
            response_user_data = None

        return response_user_data

    async def update(
            self,
            request_user_data: UserDataDB = '',
            new_user_data: UserDataDB = ''
    ) -> Optional[UserDataDB]:

        query = fill_query(update(UserDataDB), request_user_data, new_user_data)
        if query is None:
            return None

        await self.session.execute(query)
        await self.session.commit()

        return request_user_data
