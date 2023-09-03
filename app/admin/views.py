import json
from hashlib import sha256
from typing import Optional
from aiohttp.web_response import json_response
from aiohttp.web_exceptions import HTTPForbidden, HTTPBadRequest, HTTPNotImplemented, \
    HTTPNotFound
from aiohttp_apispec import request_schema, response_schema, querystring_schema
from aiohttp_session import get_session

from app.admin.models import Admin
from app.admin.schemes import AdminSchema, AdminResponseSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from tests.utils import ok_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminResponseSchema, 200)
    async def post(self):
        data = await self.request.json()
        email: Optional[str] = data.get("email", None)
        password = data.get("password", None)

        password = sha256(password.encode()).hexdigest()

        if email is None:
            raise HTTPBadRequest(text=json.dumps({"email": ["Missing data for required field."]}),
                                 reason="Email field is required")

        session = await get_session(self.request)
        session["key"] = self.request.app.config.session.key

        for user in self.store.admins.app.database.admins:
            if user.email == email and user.password == password:
                return json_response(ok_response({
                    "id": user.id,
                    "email": user.email
                }))
        raise HTTPForbidden

    async def get(self):
        raise HTTPNotImplemented


class AdminCurrentView(AuthRequiredMixin, View):
    @querystring_schema(AdminSchema)
    @response_schema(AdminResponseSchema, 200)
    async def get(self):
        admin_email = self.request.app.database.admins[0].email
        admin: Optional["Admin"] = await self.request.app.store.admins.get_by_email(email=admin_email)

        if admin:
            return json_response(ok_response({
                "id": admin.id,
                "email": admin.email
            }))
        else:
            raise HTTPNotFound
