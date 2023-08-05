__author__ = "Fábio Macêdo Mendes"
__version__ = "0.5.2"

try:
    import cytoolz as toolz
    import cytoolz.curried as ctoolz
except ImportError:
    try:
        import toolz  # noqa: F401
        import toolz.curried as ctoolz
    except ImportError:
        toolz = ctoolz = None

from . import op
from .core import *
from .functools import *
from .itertools import *
from .lazytools import *
from .magics import *
from .misc import misc
from .types import *
from .types import json


@call()
def _fix():
    # Add sidekick.json to sys.modules
    import sys

    sys.modules["sidekick.json"] = json
    return None


_ = placeholder
__all__ = ["_", *(attr for attr in globals() if not attr.startswith("_"))]
