from typing import List

from fastapi import HTTPException

from app.models.models import Admin
from app.schemas.schemas import AdminCreate, AdminUpdate
from ..repositories.admin_repository import AdminRepository


class AdminService:
    def __init__(self, admin_repository: AdminRepository) -> None:
        self.admin_repository = admin_repository

    async def get_admins(self) -> List[Admin]:
        """Retrieves all admins from the database."""
        return await self.admin_repository.get_admins()

    async def get_admin_by_id(self, admin_id: int) -> Admin:
        """Retrieves a specific admin by ID."""
        admin = await self.admin_repository.get_admin_by_id(admin_id)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return admin

    async def create_admin(self, admin_data: AdminCreate) -> Admin:
        """Creates a new admin in the database."""
        return await self.admin_repository.create_admin(admin_data)

    async def update_admin(self, admin_id: int, admin_data: AdminUpdate) -> Admin:
        """Updates an existing admin in the database."""
        return await self.admin_repository.update_admin(admin_id, admin_data)
