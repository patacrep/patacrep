from collections import UserDict

class DictOfDict(UserDict):
    """Dictionary, with a smart :meth:`update` method.

    By "smart", we mean: if `self.update(other)` is called, and for some key
    both `self[key]` and `other[key]` are dictionary, then `self[key]` is not
    replaced by `other[key]`, but instead is updated.

    >>> ordinal = DictOfDict({
    ... "francais": {
    ...     1: "premier",
    ...     2: "deuxieme",
    ...     },
    ... "english": {
    ...     1: "first",
    ...     },
    ... })
    >>> ordinal.update({
    ... "francais": {
    ...     2: "second",
    ...     3: "troisieme",
    ...     },
    ... "espanol": {
    ...     1: "primero",
    ...     },
    ... })
    >>> ordinal == {
    ...     "francais": {
    ...         1: "premier",
    ...         2: "second",
    ...         3: "troisieme",
    ...         },
    ...     "english": {
    ...         1: "first",
    ...         },
    ...     "espanol": {
    ...         1: "primero",
    ...         },
    ...     }
    True
    """

    def update(self, other):
        for key in other:
            if key not in self:
                self[key] = other[key]
            elif isinstance(self[key], dict) and isinstance(other[key], dict):
                self[key].update(other[key])
            else:
                self[key] = other[key]
