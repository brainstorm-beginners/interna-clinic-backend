from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.repositories.admin_repository import AdminRepository
from app.api.v1.services.admin_service import AdminService
from app.dependencies import get_async_session, get_admin_service
from app.schemas.schemas import AdminRead, AdminUpdate, AdminCreateRawPassword

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


    # TODO: Move this endpoint to the new 'auth' module as a part of login-registering logic.
@router.post("/admins/register", response_model=AdminCreateRawPassword)
async def register_admin(new_admin_data: AdminCreateRawPassword, admin_service: AdminService = Depends(get_admin_service)):
    """
    Creates a new admin in the database.
    """
    new_admin = await admin_service.register_admin(new_admin_data)

    return new_admin


@router.put("/{admin_id}", response_model=AdminRead)
async def update_admin(admin_id: int, admin_data: AdminUpdate, session: AsyncSession = Depends(get_async_session)):
    """
    Updates an existing admin in the database.
    """
    admin_repository = AdminRepository(session)

    admin = await admin_repository.update_admin(admin_id, admin_data)
    return admin


@router.delete("/admins/{admin_id}", response_model=None)
async def delete_admin(admin_id: int, session: AsyncSession = Depends(get_async_session)):
    admin_repository = AdminRepository(session)

    admin = await admin_repository.delete_admin(admin_id)
    return None
