"""Render `very simple` TeX commands in a simple TeX code."""

import logging

LOGGER = logging.getLogger()

MATCH = [
    # Diacritics: a
    (r"\'a", "á"),
    (r"\'A", "Á"),
    (r"\`a", "à"),
    (r"\`A", "À"),
    (r"\^a", "â"),
    (r"\^A", "Â"),
    (r"\"a", "ä"),
    (r"\"A", "Ä"),

    # Diacritics: e
    (r"\'e", "é"),
    (r"\'E", "É"),
    (r"\`e", "è"),
    (r"\`E", "È"),
    (r"\^e", "ê"),
    (r"\^E", "Ê"),
    (r"\"e", "ë"),
    (r"\"E", "Ë"),

    # Diacritics: i
    (r"\'i", "í"),
    (r"\'I", "Í"),
    (r"\`i", "ì"),
    (r"\`I", "Ì"),
    (r"\^i", "î"),
    (r"\^I", "Î"),
    (r"\"i", "ï"),
    (r"\"I", "Ï"),
    (r"\'\i", "í"),
    (r"\'\I", "Í"),
    (r"\`\i", "ì"),
    (r"\`\I", "Ì"),
    (r"\^\i", "î"),
    (r"\^\I", "Î"),
    (r"\"\i", "ï"),
    (r"\"\I", "Ï"),

    # Diacritics: o
    (r"\'o", "ó"),
    (r"\'O", "Ó"),
    (r"\`o", "ò"),
    (r"\`O", "Ò"),
    (r"\^o", "ô"),
    (r"\^O", "Ô"),
    (r"\"o", "ö"),
    (r"\"O", "Ö"),

    # Diacritics: u
    (r"\'u", "ú"),
    (r"\'U", "Ú"),
    (r"\`u", "ù"),
    (r"\`U", "Ù"),
    (r"\^u", "û"),
    (r"\^U", "Û"),
    (r"\"u", "ü"),
    (r"\"U", "Ü"),

    # Cedille
    (r"\c c", "ç"),
    (r"\c C", "Ç"),

    # œ, æ
    (r"\oe", "œ"),
    (r"\OE", "Œ"),
    (r"\ae", "æ"),
    (r"\AE", "Æ"),

    # Spaces
    (r"\ ", " "),
    (r"\,", " "),
    (r"\~", " "),

    # IeC
    (r"\IeC ", ""),

    # Miscallenous
    (r"\dots", "…"),
    (r"\%", "%"),
    (r"\&", "&"),
    (r"\_", "_"),

    ]


def detex(arg):
    """Render very simple TeX commands from argument.

    Argument can be:
    - a string: it is processed;
    - a list, dict or set: its values are processed.
    """
    if isinstance(arg, dict):
        return dict([
            (key, detex(value))
            for (key, value)
            in arg.items()
            ])
    elif isinstance(arg, list):
        return [
            detex(item)
            for item
            in arg
            ]
    elif isinstance(arg, set):
        return set(detex(list(arg)))
    elif isinstance(arg, str):
        string = arg
        for (latex, plain) in MATCH:
            string = string.replace(latex, plain)
        if '\\' in string:
            LOGGER.warning("Remaining command in string '{}'.".format(string))
        return string.strip()
    else:
        return detex(str(arg))
