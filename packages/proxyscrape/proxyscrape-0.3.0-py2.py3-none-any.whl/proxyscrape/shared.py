# MIT License
#
# Copyright (c) 2018 Jared Gillespie
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


__all__ = ['is_iterable', 'Proxy', 'request_proxy_list']


from collections import namedtuple

import requests

from .errors import (
    RequestFailedError,
    RequestNotOKError
)

Proxy = namedtuple('Proxy', ['host', 'port', 'code', 'country', 'anonymous', 'type', 'source'])


def request_proxy_list(url):
    try:
        response = requests.get(url)
    except requests.RequestException:
        raise RequestFailedError()

    if not response.ok:
        raise RequestNotOKError()
    return response


def is_iterable(obj):
    if isinstance(obj, str) or isinstance(obj, Proxy):
        return False

    try:
        iter(obj)
        return True
    except TypeError:
        return False
