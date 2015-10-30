"""Dynamic creation of test methods."""

class DynamicTest(type):
    """Metaclass that creates on-the-fly test methods.

    Each class implementing this metaclass must define two class methods:

    - `_iter_testmethods`, which iterate over `(methodname, args)`, where
      `methodname` is the name of a test method to create, and `args` is a list
      of arguments to pass to `_create_test`;
    - `_create_test`, a method returning a test method.
    """

    def __init__(cls, name, bases, nmspc):
        super().__init__(name, bases, nmspc)
        for methodname, testmethod in cls._iter_testmethods():
            setattr(cls, methodname, testmethod)

    def _iter_testmethods(cls):
        """Iterate over dynamically generated test methods."""
        raise NotImplementedError()
