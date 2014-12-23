"""
Interfaces used by sublp.
"""
import abc

class ProjectDispatchInterface(object):
    """
    Interface for dispatching on the input cases.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def dispatch_check(cls, _string, *args, **kwargs):  #pylint: disable=no-self-argument
        """
        @type: _string: str
        @returns: bool
        """
        return NotImplemented

    @abc.abstractmethod
    def form_command(cls, _string, *args, **kwargs):  #pylint: disable=no-self-argument
        """
        @type: _string: str
        @returns: str
        """
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is ProjectDispatchInterface:
            if meets(subclass, cls):
                return True
        return NotImplemented


class New_ProjectDispatchInterface(object):
    """
    Interface for dispatching on the input cases.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractproject
    def matches(self, _string):
        """
        @type: _string: str
        @returns: bool
        """
        return NotImplemented
    @abc.abstractproperty
    def command()

    def dispatch_check(self, _string, *args, **kwargs):  #pylint: disable=no-self-argument


    @abc.abstractmethod
    def form_command(cls, _string, *args, **kwargs):  #pylint: disable=no-self-argument
        """
        @type: _string: str
        @returns: str
        """
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is ProjectDispatchInterface:
            if meets(subclass, cls):
                return True
        return NotImplemented



def meets(obj, interface):
    """
    Does object meet a given interface (abstact class).
    @type: obj: object
    @type: interface: abc.ABCMeta
    @rtype: bool
    """
    return bool(list(missing_abstracts(obj, interface)))  # if no yields


def missing_abstracts(obj, interface):
    """
    Return names of all abstract methods on object, which do not have a
    concrete implementation.
    @type: obj: object
    @type: interface: abc.ABCMeta
    @rtype: iter of str
    """
    for name in interface.__abstractmethods__:
        if not has_concrete_method(obj, name):
            yield name


def has_concrete_method(obj, name):
    """
    Predicate. Does object have a non-abstract method of a given name?
    @type: obj: object
    @type: name: str
    @returns: bool
    """
    if hasattr(obj, name):
        return is_abstract_method(getattr(obj, name))
    else:
        return False

def is_abstract_method(method):
    """
    Predicate. Is a method-object abstract?
    @type: method: str
    @rtype: bool
    """
    return bool(getattr(method, '__isabstractmethod__', False))

