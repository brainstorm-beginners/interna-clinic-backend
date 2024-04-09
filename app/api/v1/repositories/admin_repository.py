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

    async def update_admin(self, new_data_for_admin: AdminUpdate) -> AdminRead:
        """
        This method is used to update the existing admin data with the new one ('AdminUpdate' model).

        Args:
            new_data_for_admin (AdminUpdate): The updated admin data.

        Returns:
            Admin: The updated admin object.

        Raises:
            HTTPException: If the admin with the given ID is not found.
        """

        admin_to_update = await self.get_admin_by_id(new_data_for_admin.id)
        if admin_to_update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        admin_to_update.update_fields(**admin_to_update.model_dump())

        await self.session.flush()
        await self.session.commit()

        return admin_to_update

    async def delete_admin(self, admin_id: int) -> int:
        """
        This method is used to delete the existing admin with given ID.

        Returns:
            deleted admin ID (int)
        """

        admin_to_delete = await self.get_admin_by_id(admin_id)
        if admin_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        await self.session.delete(admin_to_delete)
        await self.session.commit()

        return admin_id
