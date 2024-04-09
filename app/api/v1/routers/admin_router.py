from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.repositories.admin_repository import AdminRepository
from app.config.database import get_async_session
from app.schemas.schemas import AdminRead, AdminCreate, AdminUpdate

router = APIRouter(
    tags=["Admins"],
    prefix="/api/v1"
)


@router.get("/", response_model=Sequence[AdminRead])
async def get_admins(session: AsyncSession = Depends(get_async_session), page: int = 1, page_size: int = 10):
    """
    Retrieves all admins from the database
    """
    admin_repository = AdminRepository(session)

    admins = await admin_repository.get_admins()

    start = (page - 1) * page_size
    end = start + page_size

    return admins[start:end]


@router.get("/{admin_id}", response_model=AdminRead)
async def get_admin_by_id(admin_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Retrieves a specific admin by ID
    """
    admin_repository = AdminRepository(session)

    admin = await admin_repository.get_admin_by_id(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin


@router.post("/", response_model=AdminRead)
async def register_admin(admin_data: AdminCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Creates a new admin in the database.
    """
    admin_repository = AdminRepository(session)

    admin = await admin_repository.register_admin(admin_data)
    return admin


@router.put("/{admin_id}", response_model=AdminRead)
async def update_admin(admin_id: int, admin_data: AdminUpdate, session: AsyncSession = Depends(get_async_session)):
    """
    Updates an existing admin in the database.
    """
    admin_repository = AdminRepository(session)

    admin = await admin_repository.update_admin(admin_id, admin_data)
    return admin
