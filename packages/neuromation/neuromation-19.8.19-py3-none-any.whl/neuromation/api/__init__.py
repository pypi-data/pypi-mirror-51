from pathlib import Path
from typing import Awaitable, Callable, Optional

import aiohttp
from yarl import URL

from .abc import (
    AbstractDockerImageProgress,
    AbstractFileProgress,
    AbstractRecursiveFileProgress,
    ImageProgressPull,
    ImageProgressPush,
    ImageProgressStep,
    StorageProgressComplete,
    StorageProgressEnterDir,
    StorageProgressFail,
    StorageProgressLeaveDir,
    StorageProgressStart,
    StorageProgressStep,
)
from .client import Client
from .config_factory import (
    CONFIG_ENV_NAME,
    DEFAULT_API_URL,
    DEFAULT_CONFIG_PATH,
    ConfigError,
    Factory,
)
from .core import (
    DEFAULT_TIMEOUT,
    AuthenticationError,
    AuthError,
    AuthorizationError,
    ClientError,
    IllegalArgumentError,
    ResourceNotFound,
)
from .jobs import (
    Container,
    HTTPPort,
    JobDescription,
    JobStatus,
    JobStatusHistory,
    JobTelemetry,
    Resources,
    Volume,
)
from .parsing_utils import LocalImage, RemoteImage
from .storage import FileStatus, FileStatusType
from .users import Action, Permission, Share
from .utils import _ContextManager


__all__ = (
    "DEFAULT_API_URL",
    "DEFAULT_CONFIG_PATH",
    "CONFIG_ENV_NAME",
    "JobDescription",
    "JobStatus",
    "JobStatusHistory",
    "JobTelemetry",
    "Resources",
    "Volume",
    "HTTPPort",
    "Action",
    "Permission",
    "Share",
    "Client",
    "FileStatusType",
    "FileStatus",
    "Container",
    "ResourceNotFound",
    "ClientError",
    "IllegalArgumentError",
    "AuthError",
    "AuthenticationError",
    "AuthorizationError",
    "AbstractFileProgress",
    "AbstractRecursiveFileProgress",
    "AbstractDockerImageProgress",
    "StorageProgressStart",
    "StorageProgressComplete",
    "StorageProgressStep",
    "StorageProgressFail",
    "StorageProgressEnterDir",
    "StorageProgressLeaveDir",
    "ImageProgressPull",
    "ImageProgressPush",
    "ImageProgressStep",
    "RemoteImage",
    "LocalImage",
    "Factory",
    "get",
    "login",
    "login_with_token",
    "logout",
    "ConfigError",
)


def get(
    *, path: Optional[Path] = None, timeout: aiohttp.ClientTimeout = DEFAULT_TIMEOUT
) -> _ContextManager[Client]:
    return _ContextManager[Client](_get(path, timeout))


async def _get(path: Optional[Path], timeout: aiohttp.ClientTimeout) -> Client:
    return await Factory(path).get(timeout=timeout)


async def login(
    show_browser_cb: Callable[[URL], Awaitable[None]],
    *,
    url: URL = DEFAULT_API_URL,
    path: Optional[Path] = None,
    timeout: aiohttp.ClientTimeout = DEFAULT_TIMEOUT
) -> None:
    await Factory(path).login(show_browser_cb, url=url, timeout=timeout)


async def login_with_token(
    token: str,
    *,
    url: URL = DEFAULT_API_URL,
    path: Optional[Path] = None,
    timeout: aiohttp.ClientTimeout = DEFAULT_TIMEOUT
) -> None:
    await Factory(path).login_with_token(token, url=url, timeout=timeout)


async def login_headless(
    get_auth_code_cb: Callable[[URL], Awaitable[str]],
    *,
    url: URL = DEFAULT_API_URL,
    path: Optional[Path] = None,
    timeout: aiohttp.ClientTimeout = DEFAULT_TIMEOUT
) -> None:
    await Factory(path).login_headless(get_auth_code_cb, url=url, timeout=timeout)


async def logout(*, path: Optional[Path] = None) -> None:
    await Factory(path).logout()
