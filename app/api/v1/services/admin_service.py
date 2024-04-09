from typing import Sequence, Any

from fastapi import HTTPException
from passlib.context import CryptContext

from app.schemas.schemas import AdminRead, AdminCreateRawPassword, AdminCreateHashedPassword, \
    AdminUpdateRawPassword, AdminUpdateHashedPassword
from ..repositories.admin_repository import AdminRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


class AdminService:
    def __init__(self, admin_repository: AdminRepository) -> None:
        self.admin_repository = admin_repository

    async def get_admins(self) -> Sequence[AdminRead]:
        """Retrieves all admins from the database."""
        return await self.admin_repository.get_admins()

    async def get_admin_by_id(self, admin_id: int) -> AdminRead:
        """Retrieves a specific admin by ID."""
        admin = await self.admin_repository.get_admin_by_id(admin_id)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return admin

    async def register_admin(self, raw_admin_data: AdminCreateRawPassword) -> dict[str, Any]:
        """Creates a new admin in the database."""

        hashed_password = hash_password(raw_admin_data.password)

        admin_data = raw_admin_data.model_dump()
        admin_data["hashed_password"] = hashed_password
        del admin_data["password"]

        admin_with_hashed_password = AdminCreateHashedPassword(**admin_data)

        return await self.admin_repository.register_admin(admin_with_hashed_password)

    async def update_admin(self, new_data_for_admin: AdminUpdateRawPassword, admin_id: int) -> AdminRead:
        """
        This method is used to update the existing admin data with the new one ('AdminUpdateRawPassword' model).

        Returns:
            updated admin (dict[str, Any])
        """

        admin_to_update = await self.admin_repository.get_admin_by_id(admin_id)
        if admin_to_update is None:
            raise HTTPException(status_code=404, detail=f"Patient with id {admin_id} does not exist.")

        hashed_password = hash_password(new_data_for_admin.password)

        admin_data = new_data_for_admin.model_dump()
        admin_data["hashed_password"] = hashed_password
        del admin_data["password"]

        admin_with_hashed_password = AdminUpdateHashedPassword(**admin_data)

        return await self.admin_repository.update_admin(admin_with_hashed_password, admin_id)

    async def delete_admin(self, admin_id: int) -> int:
        """
            Deleting admin from the database.
        Raises:
            HTTPException: If admin not find.
        """
        try:
            admin = await self.admin_repository.delete_admin(admin_id)
            return admin
        except HTTPException as exc:
            raise exc
