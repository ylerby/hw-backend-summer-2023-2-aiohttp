from aiohttp.web import Request
from aiohttp.web_exceptions import HTTPUnauthorized


class AuthRequiredMixin:
    @staticmethod
    async def check_auth(request: Request):
        if not request.headers.get("Cookie"):
            raise HTTPUnauthorized
