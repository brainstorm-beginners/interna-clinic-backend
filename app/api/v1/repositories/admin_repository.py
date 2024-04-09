from typing import Sequence, Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.models import Admin
from app.schemas.schemas import AdminRead, AdminCreate, AdminUpdate


class AdminRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_admins(self) -> Sequence[AdminRead]:
        """
        This method is used to retrieve all admins from the DB.

        Returns:
            admins (Sequence[Admin])
        """

        data = await self.session.execute(select(Admin))
        admins = data.scalars().all()

        return admins

    async def get_admin_by_id(self, admin_id: int) -> AdminRead | None:
        """
        This method is used to retrieve a certain admin from the DB by his 'id' field.

        Returns:
            admins (Admin | None)
        """

        data = await self.session.execute(select(Admin).where(Admin.id == admin_id))
        admin = data.scalars().first()

        return admin

    # TODO: Move this endpoint to the new 'auth' module as a part of login-registering logic.
    async def register_admin(self, new_admin_data: AdminCreate) -> dict[str, Any]:
        """
        This method is used to create an admin with the given data ('AdminCreate' model).

        Returns:
            created admin (dict[str, Any])
        """

        new_admin = Admin(**new_admin_data.model_dump())
        self.session.add(new_admin)
        await self.session.flush()
        await self.session.commit()

        return new_admin

    async def update_admin(self, admin_id: int, admin: AdminUpdate) -> dict[str, Any]:
        """
        Updates an existing admin in the database with the provided information.

        Args:
            admin_id (int): The ID of the admin to be updated.
            admin (AdminUpdate): The updated admin data.

        Returns:
            Admin: The updated admin object.

        Raises:
            HTTPException: If the admin with the given ID is not found.
        """
        admin = await self.get_admins(admin_id)
        if admin is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        admin.update_fields(**admin.model_dump())

        await self.session.flush()
        await self.session.commit(admin)
        return admin

    async def delete_admin(self, admin_id: int):
        admin = await self.get_admins(admin_id)

        if admin is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        await self.session.delete(admin)
        await self.session.commit()
        return admin
