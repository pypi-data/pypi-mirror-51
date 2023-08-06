
from __future__ import annotations

__all__ = ('ManagerAttrAccessMixin',
           'TocReader',
           'bucketise',
           'slugify',
           'is_outdated',
           'setup_logging')

import asyncio
from collections import defaultdict, namedtuple
from datetime import datetime
from functools import reduce
from pathlib import Path
import re
from typing import TYPE_CHECKING
from typing import Any, Callable, Iterable, List, Tuple, Union

from . import __version__

if TYPE_CHECKING:
    from .config import Config
    from .manager import Manager


class ManagerAttrAccessMixin:

    def __getattr__(self, name: str) -> Any:
        return getattr(self.manager, name)


class TocReader:
    """Extracts key–value pairs from TOC files."""

    Entry = namedtuple('_TocEntry', 'key value')

    def __init__(self, path: Path, default: Union[None, str] = '') -> None:
        entries = (e.lstrip('# ').partition(': ')[::2]
                   for e in path.read_text(encoding='utf-8-sig').splitlines()
                   if e.startswith('## '))
        self.entries = dict(entries)
        self.default = default

    def __getitem__(self, key: Union[str, Tuple[str, ...]]) -> Entry:
        if isinstance(key, tuple):
            try:
                return next(filter(lambda i: i.value,
                                   (self.__getitem__(k) for k in key)))
            except StopIteration:
                key = key[0]
        return self.Entry(key, self.entries.get(key, self.default))


def bucketise(iterable: Iterable, key: Callable = (lambda v: v)) -> dict:
    "Place the elements of ``iterable`` into a bucket according to ``key``."
    bucket = defaultdict(list)      # type: ignore
    for value in iterable:
        bucket[key(value)].append(value)
    return dict(bucket)


def dict_merge(*args: dict) -> dict:
    "Right merge any number of ``dict``s."
    return reduce(lambda p, n: {**p, **n}, args, {})


async def gather(it: Iterable, return_exceptions: bool = True) -> List[Any]:
    return await asyncio.gather(*it, return_exceptions=return_exceptions)


_match_loweralphanum = re.compile(r'[^0-9a-z ]')


def slugify(text: str) -> str:
    "Convert an add-on name into a lower-alphanumeric slug."
    return '-'.join(_match_loweralphanum.sub(' ', text.casefold()).split())


def is_outdated(manager: Manager) -> bool:
    """Check against PyPI to see if `instawow` is outdated.

    The response is cached for 24 hours.
    """
    def parse_version(version: str) -> Tuple[int, ...]:
        return tuple(map(int, version.split('.')))

    cache_file = manager.config.config_dir / '.pypi_version'
    mtime = cache_file.exists() and cache_file.stat().st_mtime
    if mtime and (datetime.now() - datetime.fromtimestamp(mtime)).days < 1:
        version = cache_file.read_text(encoding='utf-8')
    else:
        from aiohttp.client import ClientError

        async def get_metadata() -> dict:
            url = 'https://pypi.org/pypi/instawow/json'
            async with manager.web_client.get(url) as response:
                return await response.json()

        try:
            version = manager.run(get_metadata())['info']['version']
        except ClientError:
            version = __version__
        else:
            cache_file.write_text(version, encoding='utf-8')

    # Assume cache is stale if installed version > version on PyPI
    if parse_version(__version__) > parse_version(version):
        return False
    else:
        return __version__ != version


def setup_logging(config: Config, level: Union[int, str] = 'INFO') -> int:
    from loguru import logger

    handler = {'sink': config.logger_dir / 'error.log',
               'level': level,
               'rotation': '1 MB',
               'enqueue': True}
    handler_id, = logger.configure(handlers=(handler,))
    return handler_id
