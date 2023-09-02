import json
from hashlib import sha256
from typing import Optional
from aiohttp.web_response import json_response
from aiohttp.web_exceptions import HTTPForbidden, HTTPBadRequest, HTTPUnprocessableEntity, HTTPNotImplemented, \
    HTTPNotFound
from aiohttp_apispec import docs, response_schema

from app.admin.models import Admin
from app.web.app import View
from tests.utils import ok_response


class AdminLoginView(View):
    async def post(self):
        data = await self.request.json()
        email: Optional[str] = data.get("email", None)
        password = data.get("password", None)

        password = sha256(password.encode()).hexdigest()

        if email is None:
            raise HTTPBadRequest(text=json.dumps({"email": ["Missing data for required field."]}),
                                 reason="Email field is required")

        for user in self.store.admins.app.database.admins:
            if user.email == email and user.password == password:
                return json_response(ok_response({
                    "id": user.id,
                    "email": user.email
                }))
        raise HTTPForbidden

    async def get(self):
        raise HTTPNotImplemented


class AdminCurrentView(View):
    async def get(self):
        admin_email = self.request.app.database.admins[0].email
        admin: Optional["Admin"] = self.request.app.store.admins.get_by_email(email=admin_email)

        if admin:
            return json_response(ok_response({
                "id": admin.id,
                "email": admin.email
            }))
        else:
            raise HTTPNotFound
