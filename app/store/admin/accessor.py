import typing
from hashlib import sha256
from typing import Optional

import yaml

from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):

        # TODO: создать админа по данным в config.yml здесь

        admin_email = sha256((self.app.config.admin.email).encode())
        admin_password = sha256((self.app.config.admin.password).encode())

        self.app.database.admins.append({admin_email: admin_password})

    async def disconnect(self, app: "Application"):
        self.app = None

    async def get_by_email(self, email: str) -> Optional[Admin]:
        #print(self.app.database["admins"])
        pass

    async def create_admin(self, email: str, password: str) -> Admin:
        raise NotImplementedError

