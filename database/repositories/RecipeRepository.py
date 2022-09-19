from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.dml import Update
from sqlalchemy.sql.expression import select, delete, update
from uuid import UUID, uuid4
from typing import Optional, List, Union, Any


from database.create_tables import RecipeModel


class RecipeDB:
    __tablename__ = RecipeModel.__tablename__

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

    def __init__(
            self,
            uid='',
            name='',
            images_name='',
            ingredients='',
            steps='',
            time_required='',
            portions_quantity='',
            difficulty='',
            vegetarian='',
            kitchen='',
            technology='',
            calories='',
            categories='',
            equipment=''
    ):
        self.uid = uid
        self.name = name
        self.images_name = images_name
        self.ingredients = ingredients
        self.steps = steps
        self.time_required = time_required
        self.portions_quantity = portions_quantity
        self.difficulty = difficulty
        self.vegetarian = vegetarian
        self.kitchen = kitchen
        self.technology = technology
        self.calories = calories
        self.categories = categories
        self.equipment = equipment

    def __repr__(self):
        return f'<RecipeDB(uid={self.uid}, name={self.name}, images_name={self.images_name},' \
               f'ingredients={self.ingredients}, steps={self.steps}, time_required={self.time_required},' \
               f'portions_quantity={self.portions_quantity}, difficulty={self.difficulty},' \
               f'vegetarian={self.vegetarian}, kitchen={self.kitchen}, technology={self.technology},' \
               f'calories={self.calories}, categories={self.categories}, equipment={self.equipment})>'

    __str__ = __repr__

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, RecipeDB):
            return False

        return (
            self.uid == other.uid and
            self.name == other.name and
            self.images_name == other.images_name and
            self.ingredients == other.ingredients and
            self.steps == other.steps and
            self.time_required == other.time_required and
            self.portions_quantity == other.portions_quantity and
            self.difficulty == other.difficulty and
            self.vegetarian == other.vegetarian and
            self.kitchen == other.kitchen and
            self.technology == other.technology and
            self.calories == other.calories and
            self.categories == other.categories and
            self.equipment == other.equipment
        )

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, RecipeDB):
            return False

        return (
            (self.uid == other.uid or self.uid == '') and
            (self.name == other.name or self.name == '') and
            (self.images_name == other.images_name or self.images_name == '') and
            (self.ingredients == other.ingredients or self.ingredients == '') and
            (self.steps == other.steps or self.steps == '') and
            (self.time_required == other.time_required or self.time_required == '') and
            (self.portions_quantity == other.portions_quantity or self.portions_quantity == '') and
            (self.difficulty == other.difficulty or self.difficulty == '') and
            (self.vegetarian == other.vegetarian or self.vegetarian == '') and
            (self.kitchen == other.kitchen or self.kitchen == '') and
            (self.technology == other.technology or self.technology == '') and
            (self.calories == other.calories or self.calories == '') and
            (self.categories == other.categories or self.categories == '') and
            (self.equipment == other.equipment or self.equipment == '')
        )

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, RecipeDB):
            return False

        return (
            (self.uid == other.uid or self.uid == '') and
            (self.name == other.name or self.name == '') and
            (self.images_name == other.images_name or self.images_name == '') and
            (self.ingredients == other.ingredients or self.ingredients == '') and
            (self.steps == other.steps or self.steps == '') and
            (self.time_required == other.time_required or self.time_required == '') and
            (self.portions_quantity == other.portions_quantity or self.portions_quantity == '') and
            (self.difficulty == other.difficulty or self.difficulty == '') and
            (self.vegetarian == other.vegetarian or self.vegetarian == '') and
            (self.kitchen == other.kitchen or self.kitchen == '') and
            (self.technology == other.technology or self.technology == '') and
            (self.calories == other.calories or self.calories == '') and
            (self.categories == other.categories or self.categories == '') and
            (self.equipment == other.equipment or self.equipment == '')
        )


def fill_query(
        query,
        request_recipe: RecipeDB = '',
        new_recipe: RecipeDB = ''
):
    is_query_empty = True

    if request_recipe != '':

        if request_recipe.uid != '':
            is_query_empty = False
            query = query.where(RecipeModel.uid == request_recipe.uid)

        if request_recipe.name != '':
            is_query_empty = False
            query = query.where(RecipeModel.name == request_recipe.name)

        if request_recipe.images_name != '':
            is_query_empty = False
            query = query.where(RecipeModel.images_name == request_recipe.images_name)

        if request_recipe.ingredients != '':
            is_query_empty = False
            query = query.where(RecipeModel.ingredients == request_recipe.ingredients)

        if request_recipe.steps != '':
            is_query_empty = False
            query = query.where(RecipeModel.steps == request_recipe.steps)

        if request_recipe.time_required != '':
            is_query_empty = False
            query = query.where(RecipeModel.time_required == request_recipe.time_required)

        if request_recipe.portions_quantity != '':
            is_query_empty = False
            query = query.where(RecipeModel.portions_quantity == request_recipe.portions_quantity)

        if request_recipe.difficulty != '':
            is_query_empty = False
            query = query.where(RecipeModel.difficulty == request_recipe.difficulty)

        if request_recipe.vegetarian != '':
            is_query_empty = False
            query = query.where(RecipeModel.vegetarian == request_recipe.vegetarian)

        if request_recipe.kitchen != '':
            is_query_empty = False
            query = query.where(RecipeModel.kitchen == request_recipe.kitchen)

        if request_recipe.technology != '':
            is_query_empty = False
            query = query.where(RecipeModel.technology == request_recipe.technology)

        if request_recipe.calories != '':
            is_query_empty = False
            query = query.where(RecipeModel.calories == request_recipe.calories)

        if request_recipe.categories != '':
            is_query_empty = False
            query = query.where(RecipeModel.categories == request_recipe.categories)

        if request_recipe.equipment != '':
            is_query_empty = False
            query = query.where(RecipeModel.equipment == request_recipe.equipment)

    if isinstance(query, Update):
        if is_query_empty:
            return None
        is_query_empty = True

        if new_recipe != '':

            if request_recipe.name != '':
                is_query_empty = False
                request_recipe.name = new_recipe.name
                query = query.values(name=new_recipe.name)

            if request_recipe.images_name != '':
                is_query_empty = False
                request_recipe.images_name = new_recipe.images_name
                query = query.values(images_name=new_recipe.images_name)

            if request_recipe.ingredients != '':
                is_query_empty = False
                request_recipe.ingredients = new_recipe.ingredients
                query = query.values(ingredients=new_recipe.ingredients)

            if request_recipe.steps != '':
                is_query_empty = False
                request_recipe.steps = new_recipe.steps
                query = query.values(steps=new_recipe.steps)

            if request_recipe.time_required != '':
                is_query_empty = False
                request_recipe.time_required = new_recipe.time_required
                query = query.values(time_required=new_recipe.time_required)

            if request_recipe.portions_quantity != '':
                is_query_empty = False
                request_recipe.portions_quantity = new_recipe.portions_quantity
                query = query.values(portions_quantity=new_recipe.portions_quantity)

            if request_recipe.difficulty != '':
                is_query_empty = False
                request_recipe.difficulty = new_recipe.difficulty
                query = query.values(difficulty=new_recipe.difficulty)

            if request_recipe.vegetarian != '':
                is_query_empty = False
                request_recipe.vegetarian = new_recipe.vegetarian
                query = query.values(vegetarian=new_recipe.vegetarian)

            if request_recipe.kitchen != '':
                is_query_empty = False
                request_recipe.kitchen = new_recipe.kitchen
                query = query.values(kitchen=new_recipe.kitchen)

            if request_recipe.technology != '':
                is_query_empty = False
                request_recipe.technology = new_recipe.technology
                query = query.values(technology=new_recipe.technology)

            if request_recipe.calories != '':
                is_query_empty = False
                request_recipe.calories = new_recipe.calories
                query = query.values(calories=new_recipe.calories)

            if request_recipe.categories != '':
                is_query_empty = False
                request_recipe.categories = new_recipe.categories
                query = query.values(categories=new_recipe.categories)

            if request_recipe.equipment != '':
                is_query_empty = False
                request_recipe.equipment = new_recipe.equipment
                query = query.values(equipment=new_recipe.equipment)

    if is_query_empty:
        return None

    return query


class RecipeRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, request_recipe: RecipeDB = '') -> List[Optional[RecipeDB]]:
        query = fill_query(select(RecipeModel), request_recipe)

        recipes = [
            RecipeDB(
                uid=recipe.uid,
                name=recipe.name,
                images_name=recipe.images_name,
                ingredients=recipe.ingredients,
                steps=recipe.steps,
                time_required=recipe.time_required,
                portions_quantity=recipe.portions_quantity,
                difficulty=recipe.difficulty,
                vegetarian=recipe.vegetarian,
                kitchen=recipe.kitchen,
                technology=recipe.technology,
                calories=recipe.calories,
                categories=recipe.categories,
                equipment=recipe.equipment
            ) for recipe in (await self.session.execute(query)).scalars()
        ]

        return recipes

    async def get_one(self, request_recipe: RecipeDB = '') -> Optional[RecipeDB]:
        recipes = await self.get_all(request_recipe)

        if recipes and recipes[0]:
            return recipes[0]
        return None

    async def delete(self, request_recipe: RecipeDB = '') -> Optional[RecipeDB]:
        query = fill_query(delete(RecipeDB), request_recipe)

        response_recipe = await self.get_one(request_recipe)
        await self.session.execute(query)
        await self.session.commit()

        return response_recipe

    async def add(
            self,
            request_recipes: Union[RecipeDB, List[RecipeDB]]
    ) -> Union[RecipeDB, List[RecipeDB], None]:

        if isinstance(request_recipes, RecipeDB):
            request_recipes = [request_recipes]

        for recipe in request_recipes:
            params = {}

            if recipe.uid != '':
                if isinstance(recipe.uid, str):
                    try:
                        params['uid'] = UUID(recipe.uid)
                    except ValueError:
                        raise ValueError(f'Unable to add new recipe'
                                         f'because parameter "uid" is incorrect')

                elif isinstance(recipe.uid, UUID):
                    params['uid'] = recipe.uid

                else:
                    params['uid'] = uuid4()

            if recipe.name != '':
                params['name'] = recipe.name
            else:
                raise ValueError(f'Unable to add new recipe'
                                 f'because parameter "name" does not exist')

            if recipe.images_name != '':
                params['images_name'] = recipe.images_name
            else:
                raise ValueError(f'Unable to add new recipe'
                                 f'because parameter "images_name" does not exist')

            if recipe.ingredients != '':
                params['ingredients'] = recipe.ingredients
            else:
                raise ValueError(f'Unable to add new recipe'
                                 f'because parameter "ingredients" does not exist')

            if recipe.steps != '':
                params['steps'] = recipe.steps
            else:
                raise ValueError(f'Unable to add new recipe'
                                 f'because parameter "steps" does not exist')

            if recipe.time_required != '':
                params['time_required'] = recipe.time_required
            else:
                raise ValueError(f'Unable to add new recipe'
                                 f'because parameter "time_required" does not exist')

            if recipe.portions_quantity != '':
                params['portions_quantity'] = recipe.portions_quantity
            else:
                raise ValueError(f'Unable to add new recipe'
                                 f'because parameter "portions_quantity" does not exist')

            if recipe.difficulty != '':
                params['difficulty'] = recipe.difficulty
            else:
                raise ValueError(f'Unable to add new recipe'
                                 f'because parameter "difficulty" does not exist')

            if recipe.vegetarian != '':
                params['vegetarian'] = recipe.vegetarian
            else:
                raise ValueError(f'Unable to add new recipe'
                                 f'because parameter "vegetarian" does not exist')

            if recipe.kitchen != '':
                params['kitchen'] = recipe.kitchen
            else:
                raise ValueError(f'Unable to add new recipe'
                                 f'because parameter "kitchen" does not exist')

            if recipe.technology != '':
                params['technology'] = recipe.technology
            else:
                raise ValueError(f'Unable to add new recipe'
                                 f'because parameter "technology" does not exist')

            if recipe.calories != '':
                params['calories'] = recipe.calories
            else:
                raise ValueError(f'Unable to add new recipe'
                                 f'because parameter "calories" does not exist')

            if recipe.categories != '':
                params['categories'] = recipe.categories
            else:
                raise ValueError(f'Unable to add new recipe'
                                 f'because parameter "categories" does not exist')

            if recipe.equipment != '':
                params['equipment'] = recipe.equipment
            else:
                raise ValueError(f'Unable to add new recipe'
                                 f'because parameter "equipment" does not exist')

            self.session.add(RecipeModel(**params))

        await self.session.commit()

        response_recipes = []
        for recipe in request_recipes:
            response_recipes.append(await self.get_one(recipe))

        if len(response_recipes) == 1:
            response_recipes = response_recipes[0]
        elif not len(response_recipes):
            response_recipes = None

        return response_recipes

    async def update(
            self,
            request_recipe: RecipeDB = '',
            new_recipe: RecipeDB = ''
    ) -> Optional[RecipeDB]:

        query = fill_query(update(RecipeDB), request_recipe, new_recipe)
        if query is None:
            return None

        await self.session.execute(query)
        await self.session.commit()

        return request_recipe
