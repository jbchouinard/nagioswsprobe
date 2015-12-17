#!/usr/bin/env python
# -*- coding=utf-8 -*-

import requests
from requests.exceptions import *

from nagioswsprobe.probe import ProbeError
from nagioswsprobe.probe import CRITICAL


PROTO = 'http'  # 'https'
HOST = 'google.com'


def url(path, proto=None, host=None):

    """
    Generate urls.

    Parameters
      path: path component of the url
      proto: protocol component, default: PROTO module constant
      host: host component of url, default: HOST module constant
    """

    if not proto:
        proto = PROTO
    if not host:
        host = HOST
    return proto + '://' + host + path


def get_path(path, *args, **kwargs):

    """
    Wrap requests.get to produce meaningful NAGIOS output in case of exceptions.
    """

    try:
        response = requests.get(url(path), *args, **kwargs)
    except ConnectionError:
        raise ProbeError(CRITICAL, 'NETWRK ERR')
    except Timeout:
        raise ProbeError(CRITICAL, 'TIMEOUT')
    except HTTPError:
        raise ProbeError(CRITICAL, 'HTTP ERR')
    # RequestException is the exception from which all exceptions in the
    # requests module inherit; since it is non-specific we consider it 'unknown'
    except RequestException:
        raise ProbeError(UNKNOWN, 'UNKWN REQ ERR')

    if response.status_code != 200:
        raise ProbeError(CRITICAL, 'HTTP %i' % response.status_code)

    return response


def post_path(path, *args, **kwargs):

    """
    Wrap requests.post to produce meaningful NAGIOS output in case of exceptions.
    """

    try:
        response = requests.post(url(path), *args, **kwargs)
    except ConnectionError:
        raise ProbeError(CRITICAL, 'NETWRK ERR')
    except Timeout:
        raise ProbeError(CRITICAL, 'TIMEOUT')
    except HTTPError:
        raise ProbeError(CRITICAL, 'HTTP ERR')
    # RequestException is the exception from which all exceptions in the
    # requests module inherit; since it is non-specific we consider it 'unknown'
    except RequestException:
        raise ProbeError(UNKNOWN, 'UNKWN REQ ERR')

    if response.status_code != 200:
        raise ProbeError(CRITICAL, 'HTTP %i' % response.status_code)

    return response
