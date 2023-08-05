# -*- coding: utf-8 -*-
"""
Collection of logging formatters
"""
from __future__ import absolute_import
import base64
import logging
import sys
import io
import traceback
from datetime import datetime
try:
    import json
except ImportError:
    import simplejson as json

from .compat import msgpack

if sys.version_info < (3, 0):
    SIMPLE_TYPES = (basestring, bool, dict, float, int, long, list, type(None))
else:
    SIMPLE_TYPES = (str, bool, dict, float, int, list, type(None))

DEFAULT_ENCODING = "utf-8"

FORMAT_STRING = "%Y-%m-%dT%H:%M:%S"

#: add log record attributes to skip list
SKIP_LIST = ("args", "asctime", "created", "exc_info", "filename", "funcName",
             "levelname", "levelno", "lineno", "message", "module", "msecs",
             "msg", "name", "pathname", "process", "processName",
             "relativeCreated", "thread", "threadName")


def format_timestamp(time, format_string):
    stamp = datetime.utcfromtimestamp(time)
    microseconds = (stamp.microsecond / 1000)
    return stamp.strftime(format_string) + ".%03d" % microseconds + "Z"


def format_traceback(exc_info):
    if not exc_info:
        return ""
    return "".join(traceback.format_exception(*exc_info))


class RecordFieldsMixin(object):
    def get_default_fields(self, record):
        fields = {
            "@logger": record.name,
            "@levelname": record.levelname,
            "@timestamp": format_timestamp(record.created, self.format_string),
            "message": record.getMessage(),
        }

        #: add optional tags
        if self.tags is not None:
            fields["tags"] = self.tags

        return fields

    def get_debug_fields(self, record):
        fields = {
            "@exc_info": format_traceback(record.exc_info),
            "@lineno": record.lineno,
            "@process": record.process,
            "@threadName": record.threadName
        }

        #: added in python 2.5
        if hasattr(record, "processName"):
            fields["@processName"] = record.processName

        #: added in python 2.6
        if hasattr(record, "funcName"):
            fields["@funcName"] = record.funcName

        return fields

    def get_extra_fields(self, record):
        fields = {}
        for key, value in record.__dict__.items():
            if key not in SKIP_LIST:
                if isinstance(value, SIMPLE_TYPES):
                    fields[key] = value
                else:
                    fields[key] = repr(value)
        return fields


class _SerializableFormatter(RecordFieldsMixin, logging.Formatter):
    serialize = None

    def __init__(self, *args, **kwargs):
        self.format_string = kwargs.pop("format_string", FORMAT_STRING)
        self.encoding = kwargs.pop("encoding", DEFAULT_ENCODING)
        self.tags = kwargs.pop("tags", None)
        super(_SerializableFormatter, self).__init__(self, *args, **kwargs)

    def format(self, record):
        #: add default record fields
        message = self.get_default_fields(record)

        #: add debugging and traceback information if an exception occurred
        if record.exc_info:
            message.update(self.get_debug_fields(record))

        #: add extra fields
        message.update(self.get_extra_fields(record))

        #: checks if the serialize method has been defined
        assert self.serialize is not None, (
            "%s expected method `serialize` to be present"
            % self.__class__.__name__
        )

        return self.serialize(message)


class JSONFormatter(_SerializableFormatter):
    def serialize(self, message):
        payload = json.dumps(message)
        return payload


class KeyValueFormatter(_SerializableFormatter):
    def serialize(self, message):
        output = StringIO.StringIO()
        items = []
        while len(items) != 0:
            item = items.pop()
            if (isinstance(it, list)):
                for item in it:
                    items.append(item)
            elif (isinstance(it, dict)):
                for key in it.keys():
                    items.append(it[key])
            else:
                output.write(repr(value))

        content = output.getvalue()
        stream.close()
        return content

class MessagePackFormatter(_SerializableFormatter):
    def __init__(self, *args, **kwargs):
        if not msgpack:
            raise Exception(
                "msgpack not found, please install msgpack.")
        super(MessagePackFormatter, self).__init__(*args, **kwargs)

    def serialize(self, message):
        payload = msgpack.packb(message, encoding=self.encoding, use_bin_type=True)
        if sys.version_info < (3, 0):
            return base64.b64encode(payload)
        else:
            return str(payload)
