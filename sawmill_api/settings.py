"""
Enables Sawmill settings to change at runtime dynamically.

The main idea behind this module is the ability to update
settings without having to restart the application. It
works by customizing attribute access and population.

To get started, just import the module:

>>> from sawmill_api import settings

The settings are grouped into sections. Here's an example
of accessing the settings for the `Planks` API handler:

>>> settings.Planks.chunk_read_size

Because modules are global in Python, if another handler
updates a setting, the other modules use the new value the
next time they reference it. Example:

>>> settings.Planks.chunk_read_size
8192
>>> new_planks = settings.Planks.__class__(chunk_read_size=1024)
>>> settattr(settings, 'Planks', new_planks)
>>> settings.Planks.chunk_read_size
1024
"""

import abc
import pathlib
import types
import re
import sys

import pydantic


class SettingsModule(types.ModuleType):
    """A custom module to control attribute access."""

    def populate(self, grouped_by_section: dict = None):
        """
        Create all the settings for Sawmill API.

        :param grouped_by_section: Override values for the settings.
        """
        if grouped_by_section is None:
            grouped_by_section = {}
        for name in dir(_MODULE):
            klass = getattr(_MODULE, name)
            if isinstance(klass, type) and issubclass(klass, Section):
                if klass is Section:
                    name = klass.__name__
                    section = klass
                else:
                    params = grouped_by_section.get(self.title_to_snake(name), {})
                    section = klass(**params)
                setattr(self, name, section)

    @staticmethod
    def title_to_snake(name: str) -> str:
        """Convert TitleCase names to title_case."""
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

    @staticmethod
    def title_to_dash(name: str) -> str:
        """Convert TitleNames to title-names"""
        return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()

    @staticmethod
    def dash_to_title(name: str) -> str:
        """Convert dashed-names to DashedNames"""
        return "".join(part.capitalize() for part in name.split("-"))

    def __setattr__(self, name, value):
        if not (isinstance(value, Section) or value is Section):
            raise AttributeError(f"Unknown setting type: {value}")
        super().__setattr__(name, value)

    def __iter__(self):
        for name, value in getattr(self, "__dict__").items():
            if name.startswith("_") or value is Section:
                continue
            yield name, value


class Section(abc.ABC):
    """
    A grouping of related settings.

    Sections must be Pydantic models where every field has
    a default value.
    """

    pass


class Planks(pydantic.BaseModel, Section):
    chunk_read_size: int = 8192
    log_root: pathlib.Path = pathlib.Path("/var/log")


# Replace the real module with the custom one.
_MODULE = sys.modules[__name__]
sys.modules[__name__] = SettingsModule(__name__)
sys.modules[__name__].populate()
