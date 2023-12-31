import typing
from typing import Optional
from hashlib import sha256
from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        self.app = app
        self.app.database.admins.append(Admin(id=self.app.database.next_admin_id, email=self.app.config.admin.email,
                                              password=self.app.config.admin.password))

    async def disconnect(self, app: "Application"):
        self.app = None

    async def get_by_email(self, email: str) -> Optional[Admin]:
        for admin in self.app.database.admins:
            if admin.email == email:
                admin.password = sha256(admin.password.encode()).hexdigest()
                return admin
        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        password = sha256(password.encode()).hexdigest()
        new_admin = Admin(email=email, password=password, id=self.app.database.next_admin_id)
        self.app.database.admins.append(new_admin)
        return new_admin
