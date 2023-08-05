# -*- coding: utf-8 -*-
import asyncio
import inspect
from collections import OrderedDict
from functools import wraps

from .mask import Mask, apply as apply_mask
from .utils import unpack


def marshal(data, fields, envelope=None, skip_none=False, mask=None):
    """Takes raw data (in the form of a dict, list, object) and a dict of
    fields to output and filters the data based on those fields.

    :param data: the actual object(s) from which the fields are taken from
    :param fields: a dict of whose keys will make up the final serialized
                   response output
    :param envelope: optional key that will be used to envelop the serialized
                     response
    :param bool skip_none: optional key will be used to eliminate fields
                           which value is None or the field's key not
                           exist in data


    >>> from flask_restplus import fields, marshal
    >>> data = { 'a': 100, 'b': 'foo', 'c': None }
    >>> mfields = { 'a': fields.Raw, 'c': fields.Raw, 'd': fields.Raw }

    >>> marshal(data, mfields)
    OrderedDict([('a', 100), ('c', None), ('d', None)])

    >>> marshal(data, mfields, envelope='data')
    OrderedDict([('data', OrderedDict([('a', 100), ('c', None), ('d', None)]))])

    >>> marshal(data, mfields, skip_none=True)
    OrderedDict([('a', 100)])

    """

    def make(cls):
        if isinstance(cls, type):
            return cls()
        return cls

    mask = mask or getattr(fields, '__mask__', None)
    fields = getattr(fields, 'resolved', fields)
    if mask:
        fields = apply_mask(fields, mask, skip=True)

    if isinstance(data, (list, tuple)):
        out = [marshal(d, fields, skip_none=skip_none) for d in data]
        if envelope:
            out = OrderedDict([(envelope, out)])
        return out

    items = ((k, marshal(data, v, skip_none=skip_none) if isinstance(v, dict)
              else make(v).output(k, data))
             for k, v in fields.items())

    if skip_none:
        items = ((k, v) for k, v in items if v is not None and v != OrderedDict())

    out = OrderedDict(items)

    if envelope:
        out = OrderedDict([(envelope, out)])

    return out


class marshal_with(object):
    """A decorator that apply marshalling to the return values of your methods.

    >>> from flask_restplus import fields, marshal_with
    >>> mfields = { 'a': fields.Raw }
    >>> @marshal_with(mfields)
    ... def get():
    ...     return { 'a': 100, 'b': 'foo' }
    ...
    ...
    >>> get()
    OrderedDict([('a', 100)])

    >>> @marshal_with(mfields, envelope='data')
    ... def get():
    ...     return { 'a': 100, 'b': 'foo' }
    ...
    ...
    >>> get()
    OrderedDict([('data', OrderedDict([('a', 100)]))])

    >>> mfields = { 'a': fields.Raw, 'c': fields.Raw, 'd': fields.Raw }
    >>> @marshal_with(mfields, skip_none=True)
    ... def get():
    ...     return { 'a': 100, 'b': 'foo', 'c': None }
    ...
    ...
    >>> get()
    OrderedDict([('a', 100)])

    see :meth:`flask_restplus.marshal`
    """
    def __init__(self, fields, envelope=None, skip_none=False, mask=None, mask_header=None):
        """
        :param fields: a dict of whose keys will make up the final
                       serialized response output
        :param envelope: optional key that will be used to envelop the serialized
                         response
        """
        self.fields = fields
        self.envelope = envelope
        self.skip_none = skip_none
        self.mask = Mask(mask, skip=True)
        self.mask_header = mask_header

    def __call__(self, f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            request = args[0]
            resp = f(*args, **kwargs)
            mask = self.mask

            if self.mask_header:
                mask = request.headers.get(self.mask_header) or mask
            while inspect.isawaitable(resp):
                resp = await resp
            if isinstance(resp, tuple):
                data, code, headers = unpack(resp)
                return marshal(data, self.fields, self.envelope, self.skip_none, mask), code, headers
            else:
                return marshal(resp, self.fields, self.envelope, self.skip_none, mask)
        return wrapper


class marshal_with_field(object):
    """
    A decorator that formats the return values of your methods with a single field.

    >>> from flask_restplus import marshal_with_field, fields
    >>> @marshal_with_field(fields.List(fields.Integer))
    ... def get():
    ...     return ['1', 2, 3.0]
    ...
    >>> get()
    [1, 2, 3]

    see :meth:`flask_restplus.marshal_with`
    """
    def __init__(self, field):
        """
        :param field: a single field with which to marshal the output.
        """
        if isinstance(field, type):
            self.field = field()
        else:
            self.field = field

    def __call__(self, f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            resp = f(*args, **kwargs)
            while asyncio.iscoroutine(resp):
                resp = await resp
            if isinstance(resp, tuple):
                data, code, headers = unpack(resp)
                return self.field.format(data), code, headers
            return self.field.format(resp)

        return wrapper
