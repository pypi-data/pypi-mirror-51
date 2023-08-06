
from __future__ import annotations

__all__ = ('Strategies',
           'CurseResolver', 'WowiResolver', 'TukuiResolver', 'InstawowResolver')

import asyncio
from datetime import datetime
from enum import Enum
from functools import wraps
from itertools import takewhile
from typing import TYPE_CHECKING
from typing import Any, Callable, ClassVar, Dict, List, Optional, Set, Tuple, Union

from loguru import logger
from yarl import URL

from . import exceptions as E
from .models import Pkg, PkgOptions
from .utils import ManagerAttrAccessMixin, gather, slugify

try:
    from functools import singledispatchmethod      # type: ignore
except ImportError:
    from singledispatchmethod import singledispatchmethod

if TYPE_CHECKING:
    from .manager import Manager


_sentinel = object()


class Strategies(str, Enum):

    default = 'default'
    latest = 'latest'

    @classmethod
    def validate(cls, method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self, *args, **kwargs) -> Callable:
            strategy = kwargs.pop('strategy')

            try:
                strategy_enum = cls[strategy]
            except KeyError:
                pass
            else:
                if strategy_enum in self.strategies:
                    return method(self, *args, **{**kwargs, 'strategy': strategy_enum})
            raise E.PkgStrategyUnsupported(strategy)

        return wrapper


class Resolver(ManagerAttrAccessMixin):

    origin: ClassVar[str]
    name: ClassVar[str]
    strategies: ClassVar[Set[Strategies]]

    def __init__(self, *, manager: Manager) -> None:
        self.manager = manager

    @classmethod
    def decompose_url(cls, uri: str) -> Optional[Tuple[str, str]]:
        "Break a URL down to its component `origin` and `id`."
        raise NotImplementedError

    async def resolve(self, id_or_slug: Union[List[str], str], *,
                      strategy: Any) -> Union[Pkg, List[Pkg]]:
        "Turn an ID or slug into a `Pkg`."
        raise NotImplementedError


class CurseResolver(Resolver):

    origin = 'curse'
    name = 'CurseForge'
    strategies = {Strategies.default, Strategies.latest}

    addon_url = URL('https://www.curseforge.com/wow/addons')
    # https://twitchappapi.docs.apiary.io/
    addon_api_url = URL('https://addons-ecs.forgesvc.net/api/v2/addon/')

    @classmethod
    def decompose_url(cls, uri: str) -> Optional[Tuple[str, str]]:
        url = URL(uri)
        if url.host == 'www.wowace.com' \
                and len(url.parts) > 2 \
                and url.parts[1] == 'projects':
            return (cls.origin, url.parts[2])
        elif url.host == 'www.curseforge.com' \
                and len(url.parts) > 3 \
                and url.parts[1:3] == ('wow', 'addons'):
            return (cls.origin, url.parts[3])

    async def _fetch(self, ids: List[str]) -> dict:
        from lxml.html import document_fromstring

        async def extract_id(id_or_slug) -> str:
            url = self.addon_url / id_or_slug
            async with self.web_client.get(url) as response:
                if response.status == 404:
                    id_ = id_or_slug
                else:
                    html = document_fromstring(await response.text())
                    id_, = html.xpath('//span[text() = "Project ID"]'
                                      '/following-sibling::span'
                                      '/text()')
                return id_

        extracted = await gather((extract_id(i) for i in ids), False)
        shortlist = list(filter(str.isdigit, extracted))
        async with self.web_client.post(self.addon_api_url, json=shortlist) as response:
            if response.status == 404:
                metadata = []       # type: ignore
            else:
                metadata = await response.json()

        results = dict.fromkeys(extracted)
        for r in metadata:
            id_ = str(r['id'])
            if id_ in results:
                results[id_] = r
            else:
                logger.info(f'extraneous id {id_!r} in results')
        return dict(zip(ids, results.values()))

    @singledispatchmethod
    @Strategies.validate
    async def resolve(self, ids: List[str], *, strategy: Strategies) -> List[Pkg]:
        results = await gather(self.resolve(k, strategy=strategy, _metadata=v)
                               for k, v in (await self._fetch(ids)).items())
        return results

    @resolve.register
    @Strategies.validate
    async def _(self, id_or_slug: str, *, strategy: Strategies,
                _metadata: Any = _sentinel) -> Pkg:
        if _metadata is _sentinel:
            pkg, = await self.resolve([id_or_slug], strategy=strategy)
            return pkg
        else:
            metadata = _metadata

        if not metadata:
            raise E.PkgNonexistent
        elif not metadata['latestFiles']:
            raise E.PkgFileUnavailable('no files available for download')

        flavor = 'wow_classic' if self.config.is_classic else 'wow_retail'
        files = (f for f in metadata['latestFiles']
                 if not f['isAlternate']    # nolib file if true
                 and f['gameVersionFlavor'] == flavor)
        if strategy is Strategies.default:
            # 1 = stable
            # 2 = beta
            # 3 = alpha
            files = (f for f in files if f['releaseType'] == 1)
        try:
            _, file = max((f['id'], f) for f in files)
        except ValueError as error:
            raise E.PkgFileUnavailable('no files meet criteria')

        return Pkg(origin=self.origin,
                   id=metadata['id'],
                   slug=metadata['slug'],
                   name=metadata['name'],
                   description=metadata['summary'],
                   url=metadata['websiteUrl'],
                   file_id=file['id'],
                   download_url=file['downloadUrl'],
                   date_published=file['fileDate'],
                   version=file['displayName'],
                   options=PkgOptions(strategy=strategy.name))


class WowiResolver(Resolver):

    origin = 'wowi'
    name = 'WoWInterface'
    strategies = {Strategies.default}

    # https://api.mmoui.com/v3/globalconfig.json
    list_api_url = URL('https://api.mmoui.com/v3/game/WOW/filelist.json')
    details_api_url = URL('https://api.mmoui.com/v3/game/WOW/filedetails/')

    def __init__(self, *, manager: Manager) -> None:
        super().__init__(manager=manager)
        self._sync_lock = asyncio.Lock()
        self._files: Dict[str, dict] = {}

    @classmethod
    def decompose_url(cls, uri: str) -> Optional[Tuple[str, str]]:
        url = URL(uri)
        if url.host in {'wowinterface.com', 'www.wowinterface.com'} \
                and len(url.parts) == 3 \
                and url.parts[1] == 'downloads':
            if url.name == 'landing.php':
                id_ = url.query.get('fileid')
                if id_:
                    return (cls.origin, id_)
            elif url.name.startswith('info'):
                id_ = ''.join(takewhile(str.isdigit, url.name[4:]))
                if id_:
                    return (cls.origin, id_)

    async def _fetch(self, ids: List[str]) -> dict:
        async with self._sync_lock:
            if not self._files:
                async with self.web_client.get(self.list_api_url) as response:
                    files = await response.json()
                self._files = {i['UID']: i for i in files}

        strict_ids = [''.join(takewhile(str.isdigit, i)) for i in ids]
        url = self.details_api_url / f'{",".join(strict_ids)}.json'
        async with self.web_client.get(url) as response:
            if response.status == 404:
                metadata = []       # type: ignore
            else:
                metadata = await response.json()

        results = dict.fromkeys(strict_ids)
        for r in metadata:
            if r['UID'] in results:
                file = self._files[r['UID']]
                results[r['UID']] = {**file, **r}
            else:
                logger.info(f'extraneous id {r["UID"]!r} in results')
        return dict(zip(ids, results.values()))

    @singledispatchmethod
    @Strategies.validate
    async def resolve(self, ids: List[str], *, strategy: Strategies) -> List[Pkg]:
        results = await gather(self.resolve(k, strategy=strategy, _metadata=v)
                               for k, v in (await self._fetch(ids)).items())
        return results

    @resolve.register
    @Strategies.validate
    async def _(self, id_or_slug: str, *, strategy: Strategies,
                _metadata: Any = _sentinel) -> Pkg:
        if _metadata is _sentinel:
            pkg, = await self.resolve([id_or_slug], strategy=strategy)
            return pkg
        else:
            metadata = _metadata

        if not metadata:
            raise E.PkgNonexistent
        elif metadata['UIPending'] == '1':
            raise E.PkgFileUnavailable('new file awaiting approval')
        else:
            return Pkg(origin=self.origin,
                       id=metadata['UID'],
                       slug=slugify(f'{metadata["UID"]} {metadata["UIName"]}'),
                       name=metadata['UIName'],
                       description=metadata['UIDescription'],
                       url=metadata['UIFileInfoURL'],
                       file_id=metadata['UIMD5'],
                       download_url=metadata['UIDownload'],
                       date_published=metadata['UIDate'],
                       version=metadata['UIVersion'],
                       options=PkgOptions(strategy=strategy.name))


class TukuiResolver(Resolver):

    origin = 'tukui'
    name = 'Tukui'
    strategies = {Strategies.default}

    api_url = URL('https://www.tukui.org/api.php')

    @classmethod
    def decompose_url(cls, uri: str) -> Optional[Tuple[str, str]]:
        url = URL(uri)
        if url.host == 'www.tukui.org' \
                and url.path in {'/addons.php', '/download.php'}:
            id_or_slug = url.query.get('id') or url.query.get('ui')
            if id_or_slug:
                return (cls.origin, id_or_slug)

    @singledispatchmethod
    @Strategies.validate
    async def resolve(self, ids: List[str], *, strategy: Strategies) -> List[Pkg]:
        return await gather(self.resolve(i, strategy=strategy) for i in ids)

    @resolve.register
    @Strategies.validate
    async def _(self, id_or_slug: str, *, strategy: Strategies) -> Pkg:
        id_or_slug, *_ = id_or_slug.partition('-')
        is_ui = id_or_slug in {'elvui', 'tukui'}

        if is_ui:
            query = 'ui'
        elif self.config.is_classic:
            query = 'classic-addon'
        else:
            query = 'addon'
        url = self.api_url.with_query({query: id_or_slug})
        async with self.web_client.get(url) as response:
            if not response.content_length:
                raise E.PkgNonexistent
            addon = await response.json(content_type='text/html')

        return Pkg(origin=self.origin,
                   id=addon['id'],
                   slug=id_or_slug if is_ui else slugify(f'{addon["id"]} {addon["name"]}'),
                   name=addon['name'],
                   description=addon['small_desc'],
                   url=addon['web_url'],
                   file_id=addon['lastupdate'],
                   download_url=addon['url'],
                   date_published=(datetime.fromisoformat(addon['lastupdate'])
                                   if is_ui else addon['lastupdate']),
                   version=addon['version'],
                   options=PkgOptions(strategy=strategy.name))


class InstawowResolver(Resolver):

    origin = 'instawow'
    name = 'instawow'
    strategies = {Strategies.default}

    @classmethod
    def decompose_url(cls, uri: str) -> None:
        return

    @singledispatchmethod
    @Strategies.validate
    async def resolve(self, ids: List[str], *, strategy: Strategies) -> List[Pkg]:
        return await gather(self.resolve(i, strategy=strategy) for i in ids)

    @resolve.register
    @Strategies.validate
    async def _(self, id_or_slug: str, *, strategy: Strategies) -> Pkg:
        if id_or_slug not in {'0', 'weakauras-companion'}:
            raise E.PkgNonexistent

        from .manager import run_in_thread
        from .wa_updater import WaCompanionBuilder

        builder = WaCompanionBuilder(self.manager)

        return Pkg(origin=self.origin,
                   id='0',
                   slug='weakauras-companion',
                   name='WeakAuras Companion',
                   description='A WeakAuras Companion wannabe.',
                   url='https://github.com/layday/instawow',
                   file_id=await run_in_thread(builder.checksum)(),
                   download_url=builder.file_out.as_uri(),
                   date_published=datetime.now(),
                   version='1.0.0',
                   options=PkgOptions(strategy=strategy.name))
