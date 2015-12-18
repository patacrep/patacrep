"""Some utility functions"""

from collections import UserDict

from patacrep import errors, Rx

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

def yesno(string):
    """Interpret string argument as a boolean.

    May raise `ValueError` if argument cannot be interpreted.
    """
    yes_strings = ["y", "yes", "true", "1"]
    no_strings = ["n", "no", "false", "0"]
    if string.lower() in yes_strings:
        return True
    if string.lower() in no_strings:
        return False
    raise ValueError("'{}' is supposed to be one of {}.".format(
        string,
        ", ".join(["'{}'".format(string) for string in yes_strings + no_strings]),
        ))

def remove_keys(data, keys=None, recursive=True):
    """
    Remove the keys of the dict
    """
    if isinstance(data, dict):
        for key in keys:
            if key in data:
                del data[key]
        if recursive:
            for key in data:
                data[key] = remove_keys(data[key], keys, True)
        return data
    elif isinstance(data, list) and recursive:
        return [remove_keys(elt, keys, True) for elt in data]
    return data

def validate_yaml_schema(data, schema):
    """
    Check that the data respects the schema
    """
    rx_checker = Rx.Factory({"register_core_types": True})
    schema = rx_checker.make_schema(schema)

    if not isinstance(data, dict):
        data = dict(data)

    try:
        schema.validate(data)
    except Rx.SchemaMismatch as exception:
        msg = 'Could not parse songbook file:\n' + str(exception)
        raise errors.SBFileError(msg)
