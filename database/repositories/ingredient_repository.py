from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.dml import Update
from sqlalchemy.sql.expression import select, delete, update
from uuid import UUID, uuid4
from typing import Optional, List, Union, Any


from database.create_tables import IngredientModel


class IngredientDB:
    __tablename__ = IngredientModel.__tablename__

    uid: Union[UUID, str, None]
    name: str
    images_name: Union[str, None]
    categories: Union[str, None]

    def __init__(
            self,
            uid='',
            name='',
            images_name='',
            categories=''
    ):
        self.uid = uid
        self.name = name
        self.images_name = images_name
        self.categories = categories

    def __repr__(self):
        return f'<IngredientDB(uid={self.uid}, name={self.name}, images_name={self.images_name},' \
               f'categories={self.categories})>'

    __str__ = __repr__

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, IngredientDB):
            return False

        return (
            self.uid == other.uid and
            self.name == other.name and
            self.images_name == other.images_name and
            self.categories == other.categories
        )

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, IngredientDB):
            return False

        return (
            (self.uid == other.uid or self.uid == '') and
            (self.name == other.name or self.name == '') and
            (self.images_name == other.images_name or self.images_name == '') and
            (self.categories == other.categories or self.categories == '')
        )

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, IngredientDB):
            return False

        return (
            (self.uid == other.uid or self.uid == '') and
            (self.name == other.name or self.name == '') and
            (self.images_name == other.images_name or self.images_name == '') and
            (self.categories == other.categories or self.categories == '')
        )


def fill_query(
        query,
        request_ingredient: IngredientDB = '',
        new_ingredient: IngredientDB = ''
):
    is_query_empty = True

    if request_ingredient != '':

        if request_ingredient.uid != '':
            is_query_empty = False
            query = query.where(IngredientModel.uid == request_ingredient.uid)

        if request_ingredient.name != '':
            is_query_empty = False
            query = query.where(IngredientModel.name == request_ingredient.name)

        if request_ingredient.images_name != '':
            is_query_empty = False
            query = query.where(IngredientModel.images_name == request_ingredient.images_name)

        if request_ingredient.categories != '':
            is_query_empty = False
            query = query.where(IngredientModel.categories == request_ingredient.categories)

    if isinstance(query, Update):
        if is_query_empty:
            return None
        is_query_empty = True

        if new_ingredient != '':

            if request_ingredient.name != '':
                is_query_empty = False
                request_ingredient.name = new_ingredient.name
                query = query.values(name=new_ingredient.name)

            if request_ingredient.images_name != '':
                is_query_empty = False
                request_ingredient.images_name = new_ingredient.images_name
                query = query.values(images_name=new_ingredient.images_name)

            if request_ingredient.categories != '':
                is_query_empty = False
                request_ingredient.categories = new_ingredient.categories
                query = query.values(categories=new_ingredient.categories)

    if is_query_empty:
        return None

    return query


class IngredientRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, request_ingredient: IngredientDB = '') -> List[Optional[IngredientDB]]:
        query = fill_query(select(IngredientModel), request_ingredient)

        ingredients = [
            IngredientDB(
                uid=ingredient.uid,
                name=ingredient.name,
                images_name=ingredient.images_name,
                categories=ingredient.categories
            ) for ingredient in (await self.session.execute(query)).scalars()
        ]

        return ingredients

    async def get_one(self, request_ingredient: IngredientDB = '') -> Optional[IngredientDB]:
        ingredients = await self.get_all(request_ingredient)

        if ingredients and ingredients[0]:
            return ingredients[0]
        return None

    async def delete(self, request_ingredient: IngredientDB = '') -> Optional[IngredientDB]:
        query = fill_query(delete(IngredientDB), request_ingredient)

        response_recipe = await self.get_one(request_ingredient)
        await self.session.execute(query)
        await self.session.commit()

        return response_recipe

    async def add(
            self,
            request_ingredients: Union[IngredientDB, List[IngredientDB]]
    ) -> Union[IngredientDB, List[IngredientDB], None]:

        if isinstance(request_ingredients, IngredientDB):
            request_ingredients = [request_ingredients]

        for ingredient in request_ingredients:
            params = {}

            if ingredient.uid != '':
                if isinstance(ingredient.uid, str):
                    try:
                        params['uid'] = UUID(ingredient.uid)
                    except ValueError:
                        raise ValueError(f'Unable to add new ingredient'
                                         f'because parameter "uid" is incorrect')

                elif isinstance(ingredient.uid, UUID):
                    params['uid'] = ingredient.uid

                else:
                    params['uid'] = uuid4()

            if ingredient.name != '':
                params['name'] = ingredient.name
            else:
                raise ValueError(f'Unable to add new ingredient'
                                 f'because parameter "name" does not exist')

            if ingredient.images_name != '':
                params['images_name'] = ingredient.images_name
            else:
                raise ValueError(f'Unable to add new ingredient'
                                 f'because parameter "images_name" does not exist')

            if ingredient.categories != '':
                params['categories'] = ingredient.categories
            else:
                raise ValueError(f'Unable to add new ingredient'
                                 f'because parameter "categories" does not exist')

            self.session.add(IngredientModel(**params))

        await self.session.commit()

        response_ingredients = []
        for recipe in request_ingredients:
            response_ingredients.append(await self.get_one(recipe))

        if len(response_ingredients) == 1:
            response_ingredients = response_ingredients[0]
        elif not len(response_ingredients):
            response_ingredients = None

        return response_ingredients

    async def update(
            self,
            request_ingredient: IngredientDB = '',
            new_ingredient: IngredientDB = ''
    ) -> Optional[IngredientDB]:

        query = fill_query(update(IngredientDB), request_ingredient, new_ingredient)
        if query is None:
            return None

        await self.session.execute(query)
        await self.session.commit()

        return request_ingredient
