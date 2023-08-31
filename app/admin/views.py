from typing import Optional

from aiohttp.web_response import json_response
from aiohttp.web_exceptions import HTTPForbidden, HTTPBadRequest, HTTPUnprocessableEntity

from app.web.app import View
from tests.utils import ok_response


class AdminLoginView(View):
    async def post(self):
        data = await self.request.json()
        email: Optional[str] = data.get("email")
        password = data.get("password")

        # TODO: сделать в случае отсутствия email raise HTTPBadRequest, но прописать в middlewares тело ошибки!
        if email == "" or email is None:
            pass

        for user in self.store.admins.app.database.admins:
            if user.email == email and user.password == password:
                return json_response(ok_response({
                    "id": user.id,
                    "email": user.email
                }))
        raise HTTPForbidden


class AdminCurrentView(View):
    async def get(self):
        raise NotImplementedError
