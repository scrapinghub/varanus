"""Package for the varanus application

Scripts are setup in ``pyproject.toml`` with::

    [tool.poetry.scripts]

Sub-commands are setup for the Command Manager with::

    [tool.poetry.plugins]
"""
from .__version__ import __version__  # noqa app version
from .__patch__ import __patches__    # noqa monkeypatches
from .__main__ import main as app     # noqa create cli app
from .utils import see                # noqa debugging
from .api import *                    # noqa python interface
