import asyncio
from uuid import uuid4

from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.sql.sqltypes import String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import Column, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import text

from database.config import settings


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': (
        'fk__%(table_name)s__%(all_column_names)s__'
        '%(referred_table_name)s'
    ),
    'pk': 'pk__%(table_name)s'
}

engine = create_async_engine(settings.DB_PATH, encoding='utf-8')

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)


class RecipeModel(Base):
    __tablename__ = 'recipe'

    uid = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    images_name = Column(String)
    ingredients = Column(String)
    steps = Column(String)
    time_required = Column(String)
    portions_quantity = Column(String)
    difficulty = Column(String)
    vegetarian = Column(String)
    kitchen = Column(String)
    technology = Column(String)
    calories = Column(String)
    categories = Column(String)
    equipment = Column(String)


class IngredientModel(Base):
    __tablename__ = 'ingredient'

    uid = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = Column(String, default=uuid4(), unique=True)
    images_name = Column(String)
    categories = Column(String)


class UserDataModel(Base):
    __tablename__ = 'user_data'

    uid = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)


class TokenModel(Base):
    __tablename__ = 'token'

    uid = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    is_active = Column(Boolean, default=True)
    user_email = Column(
        String,
        ForeignKey(UserDataModel.email, onupdate='cascade', ondelete='cascade'),
        nullable=False
    )


# create_tables
async def main():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
    return 0


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
