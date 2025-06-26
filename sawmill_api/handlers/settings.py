from sawmill_api import utils, settings
from sawmill_api.lib import oltp

import flask
import pydantic


settings_api = flask.Blueprint("settings_api", __name__, url_prefix="/api/1/settings")
log = utils.get_logger(__name__)

# A bit long, but enables us to just add settings to module
# and auto-magically reflect them in the API. Yay automation!
SettingsAPI = pydantic.create_model(
    "SettingsAPI",
    **{
        settings.title_to_dash(section_name): settings_section.__class__
        for section_name, settings_section in list(settings)
    },
)


@settings_api.route("/", methods=["GET"])
def get_settings():
    """Read the current settings being used by Sawmill."""
    data = {}
    for section_name, current_settings in list(settings):
        data[settings.title_to_dash(section_name)] = current_settings
    return SettingsAPI(**data).model_dump_json(), 200


@settings_api.route("/<section>", methods=["PUT"])
def update_setting(section):
    """Override the default value of a setting"""
    section_name = settings.dash_to_title(section)
    instance = getattr(settings, section_name)
    current_values = instance.model_dump()
    new_values = flask.request.json
    current_values.update(new_values)
    new_instance = instance.__class__(**current_values)
    oltp.set_api_setting(new_instance)
    setattr(settings, section_name, new_instance)
    return "", 204  # no content


@settings_api.route("/<section>/<name>", methods=["DELETE"])
def default_setting(section, name):
    """Revert a setting to it's default value."""
    section_name = settings.dash_to_title(section)
    instance = getattr(settings, section_name)
    current_values = instance.model_dump()
    current_values.pop(name)
    defaulted_values = instance.__class__().model_dump()
    defaulted_values.update(current_values)
    new_instance = instance.__class__(**defaulted_values)
    oltp.set_api_setting(new_instance)
    setattr(settings, section_name, new_instance)
    return "", 204  # no content
