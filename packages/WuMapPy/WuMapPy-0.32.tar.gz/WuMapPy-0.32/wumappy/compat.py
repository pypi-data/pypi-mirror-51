# coding: utf8
"""
    wumappy.compat
    --------------

    Workarounds for compatibility with Python 3 in the same code base.

    :copyright: Copyright 2014-2019 Lionel Darras, Philippe Marty, Quentin Vitale and contributors, see AUTHORS.
    :license: BSD, see LICENSE for details.

"""

import sys

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 3.x?
is_py3 = (_ver[0] == 3)

#: Python 3.0.x
is_py30 = (is_py3 and _ver[1] == 0)

#: Python 3.1.x
is_py31 = (is_py3 and _ver[1] == 1)

#: Python 3.2.x
is_py32 = (is_py3 and _ver[1] == 2)

#: Python 3.3.x
is_py33 = (is_py3 and _ver[1] == 3)

#: Python 3.4.x
is_py34 = (is_py3 and _ver[1] == 4)

#: Python 3.5.x
is_py35 = (is_py3 and _ver[1] == 5)

#: Python 3.6.x
is_py36 = (is_py3 and _ver[1] == 6)

#: Python 3.7.x
is_py37 = (is_py3 and _ver[1] == 7)

# ---------
# Specifics
# ---------

if is_py3:
    from logging import NullHandler
    from io import StringIO

    str = str
    bytes = bytes
