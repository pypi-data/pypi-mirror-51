from __future__ import absolute_import

import datetime
import itertools
import json
from functools import partial

from six.moves import zip
from sqlalchemy import inspect, TypeDecorator, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON, JSONB
from sqlalchemy.engine.reflection import Inspector


def result_to_dict(res):
    """
    :param res: :any:`sqlalchemy.engine.ResultProxy`

    :return: a list of dicts where each dict represents a row in the query where the key \
    is the column name and the value is the value of that column.
    """
    keys = list(res.keys())
    return [dict(zip(keys, row)) for row in res]


def get_bind_processor(column_type, dialect):
    """
    Returns a bind processor for a column type and dialect, with special handling
    for JSON/JSONB column types to return dictionaries instead of serialized JSON strings.

    NOTE: This is a workaround for https://github.com/NerdWalletOSS/savage/issues/8

    :param column_type: :py:class:`~sqlalchemy.sql.type_api.TypeEngine`
    :param dialect: :py:class:`~sqlalchemy.engine.interfaces.Dialect`
    :return: bind processor for given column type and dialect
    """
    if column_type.compile(dialect) not in {"JSON", "JSONB"}:
        # For non-JSON/JSONB column types, return the column type's bind processor
        return column_type.bind_processor(dialect)

    if type(column_type) in {JSON, JSONB}:
        # For bare JSON/JSONB types, we simply skip bind processing altogether
        return None
    elif isinstance(column_type, TypeDecorator) and column_type._has_bind_processor:
        # For decorated JSON/JSONB types, we return the custom bind processor (if any)
        return partial(column_type.process_bind_param, dialect=dialect)
    else:
        # For all other cases, we fall back to deserializing the result of the bind processor
        def wrapped_bind_processor(value):
            json_deserializer = dialect._json_deserializer or json.loads
            return json_deserializer(column_type.bind_processor(dialect)(value))

        return wrapped_bind_processor


def get_column_attribute(row, col_name, use_dirty=True, dialect=None):
    """
    :param row: the row object
    :param col_name: the column name
    :param use_dirty: whether to return the dirty value of the column
    :param dialect: if not None, should be a :py:class:`~sqlalchemy.engine.interfaces.Dialect`. If \
    specified, this function will process the column attribute into the dialect type before \
    returning it; useful if one is using user defined column types in their mappers.

    :return: if :any:`use_dirty`, this will return the value of col_name on the row before it was \
    changed; else this will return getattr(row, col_name)
    """

    def identity(x):
        return x

    bind_processor = None
    if dialect:
        column_type = getattr(type(row), col_name).type
        bind_processor = get_bind_processor(column_type, dialect)
    bind_processor = bind_processor or identity
    current_value = bind_processor(getattr(row, col_name))
    if use_dirty:
        return current_value

    hist = getattr(inspect(row).attrs, col_name).history
    if not hist.has_changes():
        return current_value
    elif hist.deleted:
        return bind_processor(hist.deleted[0])
    return None


def get_column_keys(table):
    """Return a generator of names of the python attribute for the table columns."""
    return (key for key, _ in get_column_keys_and_names(table))


def get_column_names(table):
    """Return a generator of names of the name of the column in the sql table."""
    return (name for _, name in get_column_keys_and_names(table))


def get_column_keys_and_names(table):
    """
    Return a generator of tuples k, c such that k is the name of the python attribute for
    the column and c is the name of the column in the sql table.
    """
    ins = inspect(table)
    return ((k, c.name) for k, c in ins.mapper.c.items())


def get_dialect(session):
    return session.bind.dialect


def has_constraint(model, engine, *col_names):  # pragma: no cover
    """
    :param model: model class to check
    :param engine: SQLAlchemy engine
    :param col_names: the name of columns which the unique constraint should contain

    :rtype: bool
    :return: True if the given columns are part of a unique constraint on model
    """
    table_name = model.__tablename__
    if engine.dialect.has_table(engine, table_name):
        # Use SQLAlchemy reflection to determine unique constraints
        insp = Inspector.from_engine(engine)
        constraints = itertools.chain(
            (sorted(x["column_names"]) for x in insp.get_unique_constraints(table_name)),
            sorted(insp.get_pk_constraint(table_name)["constrained_columns"]),
        )
        return sorted(col_names) in constraints
    else:
        # Needed to validate test models pre-creation
        constrained_cols = set()
        for arg in getattr(model, "__table_args__", []):
            if isinstance(arg, UniqueConstraint):
                constrained_cols.update([c.name for c in arg.columns])
        for c in model.__table__.columns:
            if c.primary_key or c.unique:
                constrained_cols.add(c.name)
        return constrained_cols.issuperset(col_names)


def is_modified(row, dialect):
    """
    Has the row data been modified?

    This method inspects the row, and iterates over all columns looking for changes
    to the (processed) data, skipping over unmodified columns.

    :param row: SQLAlchemy model instance
    :param dialect: :py:class:`~sqlalchemy.engine.interfaces.Dialect`
    :return: True if any columns were modified, else False
    """
    ins = inspect(row)
    modified_cols = set(get_column_keys(ins.mapper)) - ins.unmodified
    for col_name in modified_cols:
        current_value = get_column_attribute(row, col_name, dialect=dialect)
        previous_value = get_column_attribute(row, col_name, use_dirty=False, dialect=dialect)
        if previous_value != current_value:
            return True
    return False


class SavageJSONEncoder(json.JSONEncoder):
    """Extends the default encoder to add support for serializing datetime objects.
    Currently, this uses the `datetime.isoformat()` method; the resulting string
    can be reloaded into a MySQL/Postgres TIMESTAMP column directly.
    (This was verified on MySQL 5.6 and Postgres 9.6)
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(SavageJSONEncoder, self).default(obj)


savage_json_serializer = partial(json.dumps, cls=SavageJSONEncoder)
