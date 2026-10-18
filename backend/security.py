"""HTTP Basic Authentication for the admin dashboard and API docs.

Credentials are read from the ``ADMIN_USERNAME`` and ``ADMIN_PASSWORD``
environment variables so they can be configured securely on Render. The
middleware protects the SQLAdmin dashboard (``/admin``) and the interactive
documentation (``/docs``, ``/redoc``, ``/openapi.json``).
"""

import base64
import binascii
import os
import secrets

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Request paths that require authentication.
PROTECTED_PREFIXES = ("/admin", "/docs", "/redoc", "/openapi.json")

_UNAUTHORIZED = Response(
    content="Authentication required.",
    status_code=401,
    headers={"WWW-Authenticate": 'Basic realm="Restricted"'},
)


def _is_authorized(request: Request) -> bool:
    header = request.headers.get("Authorization")
    if not header or not header.startswith("Basic "):
        return False

    try:
        decoded = base64.b64decode(header[6:]).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError):
        return False

    username, separator, password = decoded.partition(":")
    if not separator:
        return False

    # Use constant-time comparison to avoid timing attacks.
    valid_username = secrets.compare_digest(username, ADMIN_USERNAME)
    valid_password = secrets.compare_digest(password, ADMIN_PASSWORD)
    return valid_username and valid_password


class BasicAuthMiddleware(BaseHTTPMiddleware):
    """Requires HTTP Basic credentials for the protected path prefixes."""

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(PROTECTED_PREFIXES) and not _is_authorized(request):
            return _UNAUTHORIZED
        return await call_next(request)
