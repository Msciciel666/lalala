"""Scanner plugin loader."""

from importlib import import_module
import os
import pkgutil
from types import ModuleType
from typing import Dict

PLUGINS: Dict[str, ModuleType] = {}


def load_plugins() -> Dict[str, ModuleType]:
    """Dynamically import plugins with prefix ``plugin_``.

    Returns
    -------
    Dict[str, ModuleType]
        Mapping of plugin names to imported modules.
    """
    global PLUGINS
    PLUGINS.clear()
    search_path = [os.path.dirname(__file__)]
    for _, name, _ in pkgutil.iter_modules(search_path):
        if name.startswith("plugin_"):
            module = import_module(f".{name}", package=__package__)
            PLUGINS[name] = module
    return PLUGINS
