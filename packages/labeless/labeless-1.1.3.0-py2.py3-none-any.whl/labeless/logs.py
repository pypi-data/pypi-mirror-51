# -*- coding: utf-8 -*
# Labeless
# by Aliaksandr Trafimchuk
#
# Source code released under
# Creative Commons BY-NC 4.0
# http://creativecommons.org/licenses/by-nc/4.0

__author__ = 'a1ext'

import logging
from os import path


class MyStdOut(object):
    def __init__(self, func, orig):
        super(MyStdOut, self).__init__()
        self._func = func
        self._orig = orig

    def write(self, text):
        fixed = text.replace('\r', '')
        self._func(fixed)
        try:
            self._orig.write(fixed)
        except:
            pass

    def flush(self):
        try:
            self._orig.flush()
        except:
            pass

    def isatty(self):
        return False


# noinspection PyDefaultArgument
def make_logger(fn=None, default=True, dummy={}):
    """ Make logger
    :param fn: filename
    :param default: flag indicates it is a default logger
    :param dummy: should not be passed, used as static loggers map
    :return: logger instance
    """
    if isinstance(fn, basestring):
        if fn.find('/') == -1:
            fn = path.join(path.dirname(path.realpath(__file__)), '..', fn)
    else:
        fn = path.join(path.dirname(path.realpath(__file__)), '..', 'labeless.log')
    if default and None in dummy:
        return dummy[None]['instance']
    if fn in dummy:
        return dummy[fn]['instance']

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                        filename=fn, filemode='a', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    dummy[fn] = {'fn': fn, 'instance': logger}
    return logger
