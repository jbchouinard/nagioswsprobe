#!/usr/bin/env python
# -*- coding=utf-8 -*-

"""
Google example probe (checks if http://google.com/ is reachable).
"""

from nagioswsprobe import http, probe
from nagioswsprobe.probe import ProbeOK


register = probe.ProbeRegister()


@register
def probe_google():

    """
    Check Google's index
    """

    http.PROTO = 'https'
    http.HOST = 'google.com'
    http.get_path('/')
    raise ProbeOK


if __name__ == '__main__':
    probe.main(register)
