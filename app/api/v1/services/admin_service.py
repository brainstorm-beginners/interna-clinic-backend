from typing import Sequence, Any

from fastapi import HTTPException
from jose.exceptions import JWTError
from passlib.context import CryptContext

from app.schemas.schemas import AdminRead, AdminCreateRawPassword, AdminCreateHashedPassword, \
    AdminUpdateRawPassword, AdminUpdateHashedPassword
from ..auth.auth import verify_token
from ..repositories.admin_repository import AdminRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


class AdminService:
    def __init__(self, admin_repository: AdminRepository) -> None:
        self.admin_repository = admin_repository

    async def get_admins(self, token: str) -> Sequence[AdminRead]:
        """
        This method is used to retrieve all admins from the DB.

        Returns:
            admins (Sequence[AdminRead])
        """

        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient", "Doctor"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await self.admin_repository.get_admins()

    async def get_admin_by_id(self, admin_id: int, token: str) -> AdminRead:
        """
        This method is used to retrieve a certain admin from the DB by his 'id' field.

        Returns:
            admin (AdminRead | None)

        Raises:
            HTTPException (404): if the admin with given ID does not exist.
            HTTPException (403): if the role isn't admin
            JWTError: if the token isn't validate or wrong
        """

        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient", "Doctor"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        admin = await self.admin_repository.get_admin_by_id(admin_id)

        if not admin:
            raise HTTPException(status_code=404, detail=f"Admin with id {admin_id} does not exist.")

        return admin

    async def register_admin(self, raw_admin_data: AdminCreateRawPassword, token: str) -> dict[str, Any]:
        """
        This method is used to create an admin with the given data ('AdminCreateRawPassword' model).
        Moreover, this method:
        1). Hashes the raw password by creating new DICT with added 'hashed_password' field and
        deleted 'password' field. After this, it creates a new 'AdminCreateHashedPassword' object and sends it
        to the 'admin_repository'.
        2). Checking if admin with given username already exists in the DB.

        Returns:
            created admin data (dict[str, Any])

        Raises:
            HTTPException (409): if admin with given username already exists in the DB.
        """

        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient", "Doctor"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Checking if admin with provided username already exists in the DB.
        already_existing_admin_with_provided_username = await self.admin_repository.get_admin_by_username(raw_admin_data.username)
        if already_existing_admin_with_provided_username:
            raise HTTPException(status_code=409, detail=f"Admin with username {raw_admin_data.username} already exists.")

        hashed_password = hash_password(raw_admin_data.password)

        admin_data = raw_admin_data.model_dump()
        admin_data["hashed_password"] = hashed_password
        del admin_data["password"]

        admin_with_hashed_password = AdminCreateHashedPassword(**admin_data)

        return await self.admin_repository.register_admin(admin_with_hashed_password)

    async def update_admin(self, new_data_for_admin: AdminUpdateRawPassword, admin_id: int, token: str) -> AdminRead:
        """
        This method is used to update the existing admin data with the new one ('AdminUpdateRawPassword' model).

        Returns:
            updated admin (dict[str, Any])
        """

        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient", "Doctor"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        admin_to_update = await self.admin_repository.get_admin_by_id(admin_id)
        if admin_to_update is None:
            raise HTTPException(status_code=404, detail=f"Admin with id {admin_id} does not exist.")

        hashed_password = hash_password(new_data_for_admin.password)

        admin_data = new_data_for_admin.model_dump()
        admin_data["hashed_password"] = hashed_password
        del admin_data["password"]

        admin_with_hashed_password = AdminUpdateHashedPassword(**admin_data)

        return await self.admin_repository.update_admin(admin_with_hashed_password, admin_id)

    async def delete_admin(self, admin_id: int, token: str) -> dict:
        """
        This method is used to delete the existing admin with given id.

        Returns:
            A dictionary containing the deleted admin ID and a message (dict).

        Raises:
            HTTPException (404): If the admin with given ID does not exist.
        """

        try:
            user_role = verify_token(token)
            if user_role["user_role"] in ["Patient", "Doctor"]:
                raise HTTPException(status_code=403, detail="Forbidden: Unauthorized role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        admin_to_delete = await self.admin_repository.get_admin_by_id(admin_id)
        if admin_to_delete is None:
            raise HTTPException(status_code=404, detail=f"Admin with id {admin_id} does not exist.")

        await self.admin_repository.delete_admin(admin_id)

        return {"admin_id": admin_id, "message": f"Admin with id {admin_id} has been deleted."}
