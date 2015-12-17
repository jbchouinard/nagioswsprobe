#!/usr/bin/env python
# -*- coding=utf-8 -*-

"""
A small framework for writing NAGIOS probes for web sites and web services.
"""

import sys
from requests.exceptions import *
import functools

OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3


def main(probe_register):

    """
    Execute the probes in the register, print status line, and exit with appropriate exit code.
    """

    codes = []
    messages = []

    for func in probe_register._probes:
        code, msg = func()
        codes.append(code)
        messages.append(msg)

    print(' - '.join(messages))
    sys.exit(max(codes))


class ProbeRegister:

    """
    Probe register. Use the register as decorator to register probe functions.

    Usage
      register = ProbeRegister()
      @register
      def probe_dummy():
        ...
    """

    def __init__(self):
        self._probes = []

    def __call__(self, func):
        title = func.__name__.split('probe_')[1].upper()

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            try:
                func(*args, **kwargs)
                return OK, title + ' OK'
            except ProbeException, e:
                return e.code, title + ' ' + e.msg
            except:
                return UNKNOWN, title + ' UNKNOWN'

        self._probes.append(wrapped)
        return wrapped


class ProbeException(Exception):

    """
    Base abstract probe exception.
    """

    def __init__(self):
        super(ProbeException, self).__init__()


class ProbeError(ProbeException):

    """
    Raised to signify the probe has encountered an error.
    """

    def __init__(self, code, msg):
        super(ProbeError, self).__init__()
        self.code = code
        self.msg = msg


class ProbeOK(ProbeException):

    """
    Raised to signify the probe has completed succesfully
    """

    def __init__(self):
        super(ProbeOK, self).__init__()
        self.code = OK
        self.msg = 'OK'
