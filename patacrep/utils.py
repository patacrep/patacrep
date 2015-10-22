"""Some utility functions"""

from collections import UserDict

class DictOfDict(UserDict):
    """Dictionary, with a recursive :meth:`update` method.

    By "recursive", we mean: if `self.update(other)` is called, and for some
    key both `self[key]` and `other[key]` are dictionary, then `self[key]` is
    not replaced by `other[key]`, but instead is updated. This is done
    recursively (that is, `self[foo][bar][baz]` is updated with
    `other[foo][bar][baz]`, if the corresponding objects are dictionaries).

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
        # pylint: disable=arguments-differ
        self._update(self, other)

    @staticmethod
    def _update(left, right):
        """Equivalent to `left.update(right)`, with recursive update."""
        for key in right:
            if key not in left:
                left[key] = right[key]
            elif isinstance(left[key], dict) and isinstance(right[key], dict):
                DictOfDict._update(left[key], right[key])
            else:
                left[key] = right[key]
