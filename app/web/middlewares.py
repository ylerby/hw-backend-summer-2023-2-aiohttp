import json
import typing
from aiohttp_apispec.middlewares import validation_middleware
from aiohttp.web import middleware
from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity, HTTPBadRequest, \
    HTTPUnauthorized, HTTPForbidden, HTTPNotFound, HTTPNotImplemented, HTTPConflict
from app.web.utils import error_json_response
if typing.TYPE_CHECKING:
    from app.web.app import Application


HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
        return response

    except HTTPBadRequest as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=json.loads(e.text)
        )

    except HTTPUnauthorized as e:
        return error_json_response(
            http_status=401,
            status=HTTP_ERROR_CODES[401]
        )

    except HTTPForbidden as e:
        return error_json_response(
            http_status=403,
            status=HTTP_ERROR_CODES[403]
        )

    except HTTPNotFound as e:
        return error_json_response(
            http_status=404,
            status=HTTP_ERROR_CODES[404]
        )

    except HTTPNotImplemented as e:
        return error_json_response(
            http_status=405,
            status=HTTP_ERROR_CODES[405]
        )

    except HTTPConflict as e:
        return error_json_response(
            http_status=409,
            status=HTTP_ERROR_CODES[409]
        )

    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status="error"
        )

    except Exception as e:
        return error_json_response(
            http_status=500,
            status=HTTP_ERROR_CODES[500]
        )

    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400]
        )

    # TODO: обработать все исключения-наследники HTTPException и отдельно Exception, как server error
    #  использовать текст из HTTP_ERROR_CODES


def setup_middlewares(app: "Application"):
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
