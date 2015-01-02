#!/bin/python3
"""
Python2-specific version of support functions.
"""
import abc
import os

__all__ = [
    'ExistingDirectory',
    'ExistingPath',
    'ExistingFile',
    'OpenProjectCaseInterface'
]

class OpenProjectCaseInterface(object):
    """
    Interface for dispatching on the input cases.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def matches(cls, _string, *args, **kwargs):  # pylint: disable=no-self-argument
        """
        @type: _string: str
        @returns: bool
        """
        return NotImplemented

    @abc.abstractmethod
    def command(cls, _string, *args, **kwargs):  # pylint: disable=no-self-argument
        """
        @type: _string: str
        @returns: str
        """
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is OpenProjectCaseInterface:
            if meets(subclass, cls):
                return True
        return NotImplemented


def meets(obj, interface):
    """
    @type: obj: object
    @type: interface: abc.ABCMeta
    @rtype: bool
    """
    return bool(list(missing_abstracts(obj, interface)))


def missing_abstracts(obj, interface):
    """
    @type: obj: object
    @type: interface: abc.ABCMeta
    @rtype: str
    """
    for name in interface.__abstractmethods__:
        if not has_concrete_method(obj, name):
            yield name


def has_concrete_method(obj, name):
    """
    @type: obj: object
    @type: name: str
    @returns: bool
    """
    if hasattr(obj, name):
        return is_abstract_method(getattr(obj, name))
    else:
        return False


def is_abstract_method(method):
    return getattr(method, '__isabstractmethod__', False)



#==========================================================
# Support classes
#==========================================================
class ValueMeta(abc.ABCMeta):
    """
    ~ABCMeta, but allows __instancecheck__ to be cleanly overwritten.
    @todo: Copy this into an interface-related package
    """

    def __instancecheck__(cls, instance):
        if hasattr(cls, '__instancecheck__'):
            return cls.__instancecheck__(instance)
        else:
            return abc.ABCMeta.__instancecheck__(cls, instance)

    def __subclasscheck__(cls, subclass):
        if hasattr(cls, '__subclasscheck__'):
            return cls.__subclasscheck__(subclass)
        else:
            return abc.ABCMeta.__subclasscheck__(cls, subclass)


class ExistingDirectory(str):
    """
    Non-instanced type-checking class (a VOG).
    Used to confirm that
    """
    __metaclass__ = ValueMeta

    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, str):
            if os.path.isdir(instance):
                return True
        return False

class ExistingFile(str):
    """
    Non-instanced type-checking class (a VOG).
    """
    __metaclass__ = ValueMeta

    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, str):
            if os.path.isfile(instance):
                return True
        return False

ExistingPath = (ExistingDirectory, ExistingFile)
