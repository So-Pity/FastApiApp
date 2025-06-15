from typing import Optional

from sqlalchemy.orm import Session, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete
from modules.logger import logger


class Database:
    """Class for performing CRUD operations on SQLAlchemy models."""

    def __init__(self, model):
        """Initialize the Database object.

        Args:
            model: The SQLAlchemy model class to perform operations on.
        """
        self.model = model

    async def create_instance(self, session: AsyncSession, **kwargs):
        """Create a new instance of the model and add it to the session.

        Args:
            session: SQLAlchemy session object.
            **kwargs: Keyword arguments representing the attributes of the new instance.

        Returns:
            The newly created instance.
        """
        new_instance = self.model(**kwargs)
        session.add(new_instance)
        return new_instance

    async def get_instance(self, session: AsyncSession, **filter_kwargs):
        """Retrieve an instance of the model based on the provided filters.

        Args:
            session: SQLAlchemy session object.
            **filter_kwargs: Keyword arguments representing the filters for the query.

        Returns:
            The retrieved instance, or None if no instance matches the filters.
        """
        stmt = select(self.model).filter_by(**filter_kwargs)
        result = await session.execute(stmt)
        return result.scalars().first() 
    
    async def get_most_recent_instances(
        self,
        session: AsyncSession,
        return_single: Optional[bool] = False,
        **filter_kwargs) -> list | object:
        """Retrieve the most recent instance of the model based on the provided filters.

        Args:
            session: SQLAlchemy session object.
            **filter_kwargs: Keyword arguments representing the filters for the query.

        Returns:
            The retrieved instance, or None if no instance matches the filters.
        """
        stmt = select(self.model).filter_by(**filter_kwargs).order_by(self.model.id.desc())
        result = await session.execute(stmt)
        if return_single:
            return result.unique().scalars().first()
        return result.unique().scalars().all()

    async def get_all_instances(
        self,
        session: AsyncSession,
        is_active: Optional[bool] = None,
        **filter_kwargs,
    ) -> list:
        """Retrieve all instances of the model.

        Returns:
            A list of all instances of the model.
        """
        stmt = select(self.model).order_by(self.model.id)
        
        if is_active is not None:
            stmt = stmt.where(self.model.is_active == is_active)
        for key, value in filter_kwargs.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        
        res = await session.execute(stmt)
        
        return res.unique().scalars().all()

    async def update_instance(self, session: AsyncSession, where_attribute: str, where_value: str, update_kwargs: dict) -> int:
        """Update instances of the model based on the provided filters.

        Args:
            session: SQLAlchemy session object.
            where_kwargs: Dictionary representing the filters for the query.
            update_kwargs: Dictionary representing the updates to apply.

        Returns:
            The number of instances updated.
        """
        if not hasattr(self.model, where_attribute):
            logger.error(f"Attribute '{where_attribute}' does not exist in model {self.model.__name__}")
            raise AttributeError(f"Attribute '{where_attribute}' does not exist in model {self.model.__name__}")

        filter_attr = getattr(self.model, where_attribute)
        
        stmt = (
            update(self.model)
            .where(filter_attr == where_value)
            .values(**update_kwargs)
            .execution_options(synchronize_session="fetch")
        )
        try:
            result = await session.execute(stmt)
            await session.commit()

            return result.rowcount

        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Database error occurred: {e}")
            raise SQLAlchemyError(f"Database error occurred: {e}")

    async def delete_instances(self, session: Session, ids_to_delete: list):
        """Delete instances of the model based on the provided filters.

        Args:
            session: SQLAlchemy session object.
            **filter_kwargs: Keyword arguments representing the filters for the query.

        Returns:
            The number of instances deleted.
        """
        stmt = delete(self.model).where(self.model.id.in_(ids_to_delete))
        res = await session.execute(stmt)
        await session.commit()
        return res.rowcount

    async def delete_instance_by_id(self, session: Session, id: int):
        """Delete instance of the model based on the provided filters (not an atomic operation).

        Args:
            session: SQLAlchemy session object.
            **filter_kwargs: Keyword arguments representing the filters for the query.

        Returns:
            The deleted instance, or None if no instance matches the filters.
        """
        stmt = delete(self.model).where(self.model.id == id)
        res = await session.execute(stmt)
        await session.commit()
