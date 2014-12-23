"""
Ontologies used for type-checking.
Seperated from interfaces - because these are used for input checking and similar.
IE much less important, and might be dropped in the file version.
"""
import abc
import os

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
    Ex.
    assert(isinstance("/Users/", ExistingDirectory))
    assert(not isinstance("/Users__/", ExistingDirectory))
    """
    __metaclass__ = ValueMeta

    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, basestring):
            if os.path.isdir(instance):
                return True
        return False
