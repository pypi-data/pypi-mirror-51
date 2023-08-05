# coding: utf-8
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals

import contextlib
import locale
import re
import shutil
import tempfile

import six
from six.moves import urllib

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


class cached_property(object):
    """A cached property computed only once per instance

    A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Deleting the attribute resets the property.
    Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
    """  # noqa

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value

if six.PY2:
    import socket

    # An approximation of ipaddress function
    def check_ip_address(value):
        '''check_ip_address

        Look at value and see if it looks like a plain ip address

        Returns:

          4 : ipv4 address
          6 : ipv6 address
          None: not an ip address
        '''
        try:
            socket.inet_aton(value)
            return 4
        except socket.error:
            pass
        try:
            socket.inet_pton(socket.AF_INET6, value)
            return 6
        except socket.error:
            pass
        return None

else:
    import ipaddress

    def check_ip_address(value):
        try:
            return ipaddress.ip_address(value).version
        except ValueError:
            return None

if six.PY2:
    def urlunquote(s):
        encoding = locale.getpreferredencoding()
        return urllib.parse.unquote(s.encode(encoding)).decode(encoding)

    @contextlib.contextmanager
    def TemporaryDirectory():
        d = tempfile.mkdtemp()
        try:
            yield d
        finally:
            shutil.rmtree(d)
else:
    urlunquote = urllib.parse.unquote
    TemporaryDirectory = tempfile.TemporaryDirectory
