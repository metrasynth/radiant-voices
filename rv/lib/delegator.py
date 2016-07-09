"""Python port of Ruby's Delegator and SimpleDelegator

Sourced from: https://github.com/hugobast/delegator

Minor modifications to support Python 3.5

License:

The MIT License (MIT)

Copyright (c) 2013 Hugo Bastien

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


class Delegator(object):

    def __init__(self, obj):
        self.__setobj__(obj)

    def __setattr__(self, name, value):
        target = self.__getobj__()

        if name in self.__dict__:
            object.__setattr__(self, name, value)
        else:
            setattr(target, name, value)

    def __getattr__(self, name):
        target = self.__getobj__()

        if hasattr(target, name):
            if callable(getattr(target, name)):
                def _missing(*args, **kwargs):
                    return getattr(target, name)(*args, **kwargs)
            else:
                _missing = getattr(target, name)

            return _missing

        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__getobj__().__class__.__name__, name
        ))

    def __setobj__(self, obj):
        raise NotImplementedError("need to define `__setobj__'")

    def __getobj__(self):
        raise NotImplementedError("need to define `__getobj__'")

    def __eq__(self, obj):
        if obj is self:
            return True
        return self.__getobj__() == obj

    def __ne__(self, obj):
        if obj is self:
            return False
        return self.__getobj__() != obj


class SimpleDelegator(Delegator):

    def __getobj__(self):
        return self.__dict__['delegate_sd_obj']

    def __setobj__(self, obj):
        if self is obj:
            raise AttributeError("cannot delegate to self")
        self.__dict__['delegate_sd_obj'] = obj