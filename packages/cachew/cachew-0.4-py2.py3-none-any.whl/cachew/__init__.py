import typing
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound

__author__    = "Dima Gerasimov"
__copyright__ = "Dima Gerasimov"
__license__   = "mit"


import functools
import logging
from itertools import chain, islice
from datetime import datetime, date
import tempfile
from pathlib import Path
import sys
from typing import (Any, Callable, Iterator, List, NamedTuple, Optional, Tuple,
                    Type, Union, TypeVar, Generic, Sequence, Iterable, Set)
import dataclasses

import sqlalchemy # type: ignore
from sqlalchemy import Column, Table, event


if sys.version_info[1] < 7:
    from .compat import fromisoformat
else:
    fromisoformat = datetime.fromisoformat


# in case of changes in the way cachew stores data, this should be changed to discard old caches
CACHEW_FORMAT = 1


def get_logger() -> logging.Logger:
    return logging.getLogger('cachew')


T = TypeVar('T')


def ichunks(l: Iterable[T], n: int) -> Iterator[List[T]]:
    it: Iterator[T] = iter(l)
    while True:
        chunk: List[T] = list(islice(it, 0, n))
        if len(chunk) == 0:
            break
        yield chunk


class IsoDateTime(sqlalchemy.TypeDecorator):
    # in theory could use something more effecient? e.g. blob for encoded datetime and tz?
    # but practically, the difference seems to be pretty small, so perhaps fine for now
    impl = sqlalchemy.String

    @property
    def python_type(self): return datetime

    def process_literal_param(self, value, dialect): raise NotImplementedError() # make pylint happy

    def process_bind_param(self, value: Optional[datetime], dialect) -> Optional[str]:
        if value is None:
            return None
        return value.isoformat()

    def process_result_value(self, value: Optional[str], dialect) -> Optional[datetime]:
        if value is None:
            return None
        return fromisoformat(value)


# a bit hacky, but works...
class IsoDate(IsoDateTime):
    impl = sqlalchemy.String

    @property
    def python_type(self): return date

    def process_literal_param(self, value, dialect): raise NotImplementedError() # make pylint happy

    def process_result_value(self, value: Optional[str], dialect) -> Optional[date]: # type: ignore
        res = super().process_result_value(value, dialect)
        if res is None:
            return None
        return res.date()


PRIMITIVES = {
    str     : sqlalchemy.String,
    int     : sqlalchemy.Integer,
    float   : sqlalchemy.Float,
    bool    : sqlalchemy.Boolean,
    datetime: IsoDateTime,
    date    : IsoDate,
}


Types = Union[
    Type[str],
    Type[int],
    Type[float],
    Type[bool],
    Type[datetime],
    Type[date],
    Type[NamedTuple],
]

Values = Union[
    str,
    int,
    float,
    bool,
    datetime,
    date,
    NamedTuple,
]


def is_primitive(cls: Type) -> bool:
    return cls in PRIMITIVES


# https://stackoverflow.com/a/2166841/706389
def is_dataclassish(t: Type) -> bool:
    """
    >>> is_dataclassish(int)
    False
    >>> is_dataclassish(tuple)
    False
    >>> from typing import NamedTuple
    >>> class N(NamedTuple):
    ...     field: int
    >>> is_dataclassish(N)
    True
    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class D:
    ...     field: str
    >>> is_dataclassish(D)
    True
    """
    if dataclasses.is_dataclass(t):
        return True
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple:
        return False
    f = getattr(t, '_fields', None)
    if not isinstance(f, tuple):
        return False
    # pylint: disable=unidiomatic-typecheck
    return all(type(n) == str for n in f)


class CachewException(RuntimeError):
    pass


def strip_optional(cls):
    """
    >>> from typing import Optional, NamedTuple
    >>> strip_optional(Optional[int])
    (<class 'int'>, True)
    >>> class X(NamedTuple):
    ...     x: int
    >>> strip_optional(X)
    (<class 'cachew.X'>, False)
    """
    is_opt: bool = False

    if getattr(cls, '__origin__', None) == Union:
        # handles Optional
        elems = cls.__args__
        elems = [e for e in elems if e != type(None)]
        if len(elems) == 1:
            cls = elems[0] # meh
            is_opt = True
        else:
            raise CachewException(f'{cls} is unsupported!')

    return (cls, is_opt)


# release mode friendly assert
def kassert(x: bool) -> None:
    if x is False:
        raise AssertionError


NT = TypeVar('NT')
# sadly, bound=NamedTuple is not working yet in mypy
# https://github.com/python/mypy/issues/685


class NTBinder(NamedTuple):
    """
    >>> class Job(NamedTuple):
    ...    company: str
    ...    title: Optional[str]
    >>> class Person(NamedTuple):
    ...     name: str
    ...     age: int
    ...     job: Optional[Job]

    NTBinder is a helper class for inteacting with sqlite database.
    Hierarchy is flattened:
    >>> binder = NTBinder.make(Person)
    >>> [(c.name, type(c.type)) for c in binder.columns]
    ... # doctest: +NORMALIZE_WHITESPACE
    [('name',         <class 'sqlalchemy.sql.sqltypes.String'>),
     ('age',          <class 'sqlalchemy.sql.sqltypes.Integer'>),
     ('_job_is_null', <class 'sqlalchemy.sql.sqltypes.Boolean'>),
     ('job_company',  <class 'sqlalchemy.sql.sqltypes.String'>),
     ('job_title',    <class 'sqlalchemy.sql.sqltypes.String'>)]


    >>> person = Person(name='alan', age=40, job=None)

    to_row converts object to a sql-friendly tuple. job=None, so we end up with True in _job_is_null field
    >>> tuple(binder.to_row(person))
    ('alan', 40, True, None, None)

    from_row does a reverse conversion
    >>> binder.from_row(('alan', 40, True, None, None))
    Person(name='alan', age=40, job=None)

    >>> binder.from_row(('ann', 25, True, None, None, 'extra'))
    Traceback (most recent call last):
    ...
    cachew.CachewException: unconsumed items in iterator ['extra']
    """
    name     : Optional[str] # None means toplevel
    type_    : Types
    span     : int  # not sure if span should include optional col?
    primitive: bool
    optional : bool
    fields   : Sequence[Any] # mypy can't handle cyclic definition at this point :(

    @staticmethod
    def make(tp: Type, name: Optional[str]=None) -> 'NTBinder':
        tp, optional = strip_optional(tp)
        primitive = is_primitive(tp)
        if primitive:
            kassert(name is not None)  # TODO too paranoid?
        fields: Tuple[Any, ...]
        if primitive:
            fields = ()
            span = 1
        else:
            fields = tuple(NTBinder.make(tp=ann, name=fname) for fname, ann in tp.__annotations__.items())
            span = sum(f.span for f in fields) + (1 if optional else 0)
        return NTBinder(
            name=name,
            type_=tp,
            span=span,
            primitive=primitive,
            optional=optional,
            fields=fields,
        )

    @property
    def columns(self) -> List[Column]:
        return list(self.iter_columns())

    def to_row(self, obj: NT) -> Tuple[Optional[Values], ...]:
        return tuple(self._to_row(obj))

    def from_row(self, row: Iterable[Any]) -> NT:
        riter = iter(row)
        res = self._from_row(riter)
        remaining = list(islice(riter, 0, 1))
        if len(remaining) != 0:
            raise CachewException(f'unconsumed items in iterator {remaining}')
        assert res is not None  # nosec # help mypy; top level will not be None
        return res


    def _to_row(self, obj) -> Iterator[Optional[Values]]:
        if self.primitive:
            yield obj
        else:
            if self.optional:
                is_none = obj is None
                yield is_none
            else:
                is_none = False; kassert(obj is not None)  # TODO hmm, that last assert is not very symmetric...

            if is_none:
                for _ in range(self.span - 1):
                    yield None
            else:
                yield from chain.from_iterable(
                    f._to_row(getattr(obj, f.name))
                    for f in self.fields
                )

    def _from_row(self, row_iter):
        if self.primitive:
            return next(row_iter)
        else:
            if self.optional:
                is_none = next(row_iter)
            else:
                is_none = False

            if is_none:
                for _ in range(self.span - 1):
                    x = next(row_iter); kassert(x is None)  # huh. assert is kinda opposite of producing value
                return None
            else:
                return self.type_(*(
                    f._from_row(row_iter)
                    for f in self.fields
                ))

    # TODO not sure if we want to allow optionals on top level?
    def iter_columns(self) -> Iterator[Column]:
        used_names: Set[str] = set()

        def col(name: str, tp) -> Column:
            while name in used_names:
                name = '_' + name
            used_names.add(name)
            return Column(name, tp)

        if self.primitive:
            if self.name is None: raise AssertionError
            yield col(self.name, PRIMITIVES[self.type_])
        else:
            prefix = '' if self.name is None else self.name + '_'
            if self.optional:
                yield col(f'_{prefix}is_null', sqlalchemy.Boolean)
            for f in self.fields:
                for c in f.iter_columns():
                    yield col(f'{prefix}{c.name}', c.type)

    def __str__(self):
        lines = ['  ' * level + str(x.name) + ('?' if x.optional else '') + ' '  + str(x.span) for level, x in self.flatten()]
        return '\n'.join(lines)

    def __repr__(self):
        return str(self)

    def flatten(self, level=0):
        yield (level, self)
        for f in self.fields:
            yield from f.flatten(level=level + 1)


# TODO better name to represent what it means?
SourceHash = str


class DbHelper:
    def __init__(self, db_path: Path, cls: Type) -> None:
        self.engine = sqlalchemy.create_engine(f'sqlite:///{db_path}')
        self.connection = self.engine.connect()

        """
        Erm... this is pretty confusing.
        https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#transaction-isolation-level

        Somehow without this thing sqlalchemy logs BEGIN (implicit) instead of BEGIN TRANSACTION which actually works in sqlite...

        Judging by sqlalchemy/dialects/sqlite/base.py, looks like some sort of python sqlite driver problem??
        """
        @event.listens_for(self.connection, "begin")
        # pylint: disable=unused-variable
        def do_begin(conn):
            conn.execute("BEGIN")

        self.meta = sqlalchemy.MetaData(self.connection)
        self.table_hash = Table('hash', self.meta, Column('value', sqlalchemy.String))
        self.table_hash.create(self.connection, checkfirst=True)

        self.binder = NTBinder.make(tp=cls)
        self.table_data = Table('table', self.meta, *self.binder.columns)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.connection.close()


HashFunction = Callable[..., SourceHash]


def default_hash(*args, **kwargs) -> SourceHash:
    return str(args + tuple(sorted(kwargs.items()))) # good enough??


# TODO give it as an example in docs
def mtime_hash(path: Path, *args, **kwargs) -> SourceHash:
    mt = path.stat().st_mtime
    return default_hash(f'{path}.{mt}', *args, **kwargs)


Failure = str


# pylint: disable=too-many-return-statements
def infer_type(func) -> Union[Failure, Type[Any]]:
    """
    >>> from typing import Collection, NamedTuple
    >>> class Person(NamedTuple):
    ...     name: str
    ...     age: int
    >>> def person_provider() -> Collection[Person]:
    ...     return []
    >>> infer_type(person_provider)
    <class 'cachew.Person'>
    """
    rtype = getattr(func, '__annotations__', {}).get('return', None)
    if rtype is None:
        return f"no return type annotation on {func}"

    def bail(reason):
        return f"can't infer type from {rtype}: " + reason

    # need to get erased type, otherwise subclass check would fail
    if not hasattr(rtype, '__origin__'):
        return bail("expected __origin__")
    if not issubclass(rtype.__origin__, Iterable):
        return bail("not subclassing Iterable")

    args = getattr(rtype, '__args__', None)
    if args is None:
        return bail("has no __args__")
    if len(args) != 1:
        return bail(f"wrong number of __args__: {args}")
    arg = args[0]
    if not is_dataclassish(arg):
        return bail(f"{arg} is not NamedTuple")
    return arg


# https://stackoverflow.com/questions/653368/how-to-create-a-python-decorator-that-can-be-used-either-with-or-without-paramet
def doublewrap(f):
    @functools.wraps(f)
    def new_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return f(args[0])
        else:
            # decorator arguments
            return lambda realf: f(realf, *args, **kwargs)
    return new_dec


PathIsh = Union[Path, str]
PathProvider = Union[PathIsh, Callable[..., PathIsh]]


@doublewrap
# pylint: disable=too-many-arguments
def cachew(
        func=None,
        cache_path: Optional[PathProvider]=None,
        cls=None,
        hashf: HashFunction=default_hash,
        logger=None,
        chunk_by=10000, # TODO dunno maybe remove it?
):  # TODO what's a reasonable default?):
    r"""
    Database-backed cache decorator. TODO more description?
    # TODO use this doc in readme?

    :param cache_path: if not set, it will be generated in `/tmp` based on function name. It is recommended to always set this parameter.
    :param cls: if not set, cachew will attempt to infer it from return type annotation. See :func:`infer_type` and :func:`cachew.tests.test_cachew.test_return_type_inference`.
    :param hashf: hash function to determine whether the. Can potentially benefit from the use of side effects (e.g. file modification time). TODO link to test?
    :param logger: custom logger, if not specified will use logger named `cachew`. See :func:`get_logger`.
    :return: iterator over original or cached items

    Usage example:
    >>> from typing import NamedTuple, Iterator
    >>> class Link(NamedTuple):
    ...     url : str
    ...     text: str
    ...
    >>> @cachew
    ... def extract_links(archive: str) -> Iterator[Link]:
    ...     for i in range(5):
    ...         import time; time.sleep(1) # simulate slow IO
    ...         yield Link(url=f'http://link{i}.org', text=f'text {i}')
    ...
    >>> list(extract_links(archive='wikipedia_20190830.zip')) # that would take about 5 seconds on first run
    [Link(url='http://link0.org', text='text 0'), Link(url='http://link1.org', text='text 1'), Link(url='http://link2.org', text='text 2'), Link(url='http://link3.org', text='text 3'), Link(url='http://link4.org', text='text 4')]

    >>> from timeit import Timer
    >>> res = Timer(lambda: list(extract_links(archive='wikipedia_20190830.zip'))).timeit(number=1) # second run is cached, so should take less time
    >>> print(f"took {int(res)} seconds to query cached items")
    took 0 seconds to query cached items
    """

    # func is optional just to make pylint happy https://github.com/PyCQA/pylint/issues/259
    # kassert(func is not None)

    if logger is None:
        logger = get_logger()

    if cache_path is None:
        td = Path(tempfile.gettempdir()) / 'cachew'
        td.mkdir(parents=True, exist_ok=True)
        cache_path = td
        logger.info('No db_path specified, using %s as implicit cache', cache_path)

    if not callable(cache_path):
        cache_path = Path(cache_path)
        if cache_path.exists() and cache_path.is_dir():
            cache_path = cache_path / str(func.__qualname__)

    inferred = infer_type(func)
    if isinstance(inferred, Failure):
        msg = f"failed to infer cache type: {inferred}"
        if cls is None:
            raise CachewException(msg)
        else:
            # it's ok, assuming user knows better
            logger.debug(msg)
    else:
        if cls is None:
            logger.debug("using inferred type %s", inferred)
            cls = inferred
        else:
            if cls != inferred:
                logger.warning("inferred type %s mismatches specified type %s", inferred, cls)
                # TODO not sure if should be more serious error...
    kassert(is_dataclassish(cls))

    return cachew_impl(
        func=func,
        cache_path=cache_path,
        cls=cls,
        hashf=hashf,
        logger=logger,
        chunk_by=chunk_by,
    )


def cachew_impl(*, func: Callable, cache_path: PathProvider, cls: Type, hashf: HashFunction, logger: logging.Logger, chunk_by: int):
    def composite_hash(*args, **kwargs) -> SourceHash:
        return f'cachew: {CACHEW_FORMAT}, schema: {cls.__annotations__}, hash: {hashf(*args, **kwargs)}'

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        dbp: Path
        if callable(cache_path):
            dbp = Path(cache_path(*args, **kwargs))  # type: ignore
        else:
            dbp = Path(cache_path)

        logger.debug('using %s for db cache', dbp)

        if not dbp.parent.exists():
            raise CachewException(f"{dbp.parent} doesn't exist") # otherwise, sqlite error is quite cryptic

        # TODO make sure we have exclusive write lock
        with DbHelper(dbp, cls) as db:
            binder = db.binder
            conn = db.connection
            values_table = db.table_data

            prev_hashes = conn.execute(db.table_hash.select()).fetchall()
            if len(prev_hashes) > 1:
                raise CachewException(f'Multiple hashes! {prev_hashes}')

            prev_hash: Optional[SourceHash]
            if len(prev_hashes) == 0:
                prev_hash = None
            else:
                prev_hash = prev_hashes[0][0]  # returns a tuple...

            logger.debug('old hash: %s', prev_hash)
            h = composite_hash(*args, **kwargs); kassert(h is not None) # just in case
            logger.debug('new hash: %s', h)

            with conn.begin():
                if h == prev_hash:
                    logger.debug('hash matched: loading from cache')
                    rows = conn.execute(values_table.select())
                    for row in rows:
                        yield binder.from_row(row)
                else:
                    logger.debug('hash mismatch: computing data and writing to db')

                    # drop and create to incorporate schema changes
                    values_table.drop(conn, checkfirst=True)
                    values_table.create(conn)

                    datas = func(*args, **kwargs)

                    for chunk in ichunks(datas, n=chunk_by):
                        bound = [binder.to_row(c) for c in chunk]
                        # pylint: disable=no-value-for-parameter
                        conn.execute(values_table.insert().values(bound))
                        yield from chunk

                    # TODO insert and replace instead?

                    # pylint: disable=no-value-for-parameter
                    conn.execute(db.table_hash.delete())
                    # pylint: disable=no-value-for-parameter
                    conn.execute(db.table_hash.insert().values([{'value': h}]))
    return wrapper


__all__ = ['cachew', 'CachewException', 'SourceHash', 'HashFunction', 'get_logger', 'NTBinder']
