from typing import Sequence, Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.models import Admin
from app.schemas.schemas import AdminRead, AdminCreateHashedPassword, AdminUpdateHashedPassword


class AdminRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_admins(self) -> Sequence[AdminRead]:
        """
        This method is used to retrieve all admins from the DB.

        Returns:
            admins (Sequence[AdminRead])
        """

        data = await self.session.execute(select(Admin))
        admins = data.scalars().all()

        return admins

    async def get_admin_by_id(self, admin_id: int) -> AdminRead | None:
        """
        This method is used to retrieve a certain admin from the DB by his 'id' field.

        Returns:
            admin (AdminRead | None)
        """

        data = await self.session.execute(select(Admin).where(Admin.id == admin_id))
        admin = data.scalars().first()

        return admin

    async def get_admin_by_username(self, admin_username: str) -> AdminRead | None:
        """
        This method is used to retrieve a certain admin from the DB by 'username' field.

        Returns:
            admin (AdminRead | None)
        """

        data = await self.session.execute(select(Admin).where(Admin.username == admin_username))
        admin = data.scalars().first()

        return admin

    async def register_admin(self, new_admin_data: AdminCreateHashedPassword) -> dict[str, Any]:
        """
        This method is used to create an admin with the given data ('AdminCreateHashedPassword' model).

        Returns:
            created admin data (dict[str, Any])
        """

        new_admin = Admin(**new_admin_data.model_dump())
        self.session.add(new_admin)
        await self.session.flush()
        await self.session.commit()

        return new_admin

    async def update_admin(self, new_data_for_admin: AdminUpdateHashedPassword, admin_id: int) -> AdminRead:
        """
        This method is used to update the existing admin data with the new one ('AdminUpdate' model).

        Args:
            new_data_for_admin (AdminUpdateHashedPassword): The new data of admin to be updated.
            admin_id (int): An ID of admin to be updated.

        Returns:
            admin (AdminRead)

        Raises:
            HTTPException: If the admin with the given ID is not found.
        """

        admin_to_update = await self.get_admin_by_id(admin_id)

        for key, value in new_data_for_admin.model_dump().items():
            setattr(admin_to_update, key, value)

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
