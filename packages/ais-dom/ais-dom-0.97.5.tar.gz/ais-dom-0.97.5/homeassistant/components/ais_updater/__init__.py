"""
Support to check for available updates.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/updater/
"""
# pylint: disable=no-name-in-module, import-error
import asyncio
from datetime import timedelta
from distutils.version import StrictVersion
import json
import logging
import os
import platform
import uuid

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.const import ATTR_FRIENDLY_NAME
from homeassistant.const import __version__ as current_version
from homeassistant.helpers import event
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
from homeassistant.ais_dom import ais_global

REQUIREMENTS = ["distro==1.3.0"]

_LOGGER = logging.getLogger(__name__)

ATTR_RELEASE_NOTES = "release_notes"

CONF_REPORTING = "reporting"
CONF_COMPONENT_REPORTING = "include_used_components"

DOMAIN = "ais_updater"
SERVICE_CHECK_VERSION = "check_version"
ENTITY_ID = "sensor.version_info"

UPDATER_URL = "https://powiedz.co/ords/dom/dom/updater"
UPDATER_UUID_FILE = ".uuid"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: {
            vol.Optional(CONF_REPORTING, default=True): cv.boolean,
            vol.Optional(CONF_COMPONENT_REPORTING, default=False): cv.boolean,
        }
    },
    extra=vol.ALLOW_EXTRA,
)

RESPONSE_SCHEMA = vol.Schema(
    {
        vol.Required("version"): cv.string,
        vol.Required("release-notes"): cv.string,
        vol.Optional("reinstall-android"): cv.boolean,
        vol.Optional("apt"): cv.string,
        vol.Optional("beta"): cv.boolean,
    }
)


def _create_uuid(hass, filename=UPDATER_UUID_FILE):
    """Create UUID and save it in a file."""
    with open(hass.config.path(filename), "w") as fptr:
        _uuid = uuid.uuid4().hex
        fptr.write(json.dumps({"uuid": _uuid}))
        return _uuid


def _load_uuid(hass, filename=UPDATER_UUID_FILE):
    """Load UUID from a file or return None."""
    try:
        with open(hass.config.path(filename)) as fptr:
            jsonf = json.loads(fptr.read())
            return uuid.UUID(jsonf["uuid"], version=4).hex
    except (ValueError, AttributeError):
        return None
    except FileNotFoundError:
        return _create_uuid(hass, filename)


async def async_setup(hass, config):
    """Set up the updater component."""

    config = config.get(DOMAIN, {})
    if config.get(CONF_REPORTING):
        huuid = await hass.async_add_job(_load_uuid, hass)
    else:
        huuid = None

    include_components = config.get(CONF_COMPONENT_REPORTING)

    async def check_new_version(now):
        say_it = False
        # check if we have datetime.datetime or call.data object
        if type(now) == "ServiceCall":
            if "say" in now.data:
                say_it = now.data["say"]
        """Check if a new version is available and report if one is."""
        result = await get_newest_version(hass, huuid, include_components)

        if result is None:
            return

        newest, releasenotes, android, apt = result
        beta = False
        if "BETA" in releasenotes:
            beta = True

        # Load data from supervisor on hass.io
        if hass.components.hassio.is_hassio():
            newest = hass.components.hassio.get_homeassistant_version()

        # Validate version
        if StrictVersion(newest) > StrictVersion(current_version):
            _LOGGER.info("The latest available version is %s", newest)
            info = "Dostępna jest nowa wersja " + newest + ". " + releasenotes
            info_for_screen = info.replace("Naciśnij OK aby zainstalować.", "")
            info_for_screen = info_for_screen.replace(
                "Naciśnij OK/URUCHOM aby zainstalować.", ""
            )
            hass.states.async_set(
                ENTITY_ID,
                info,
                {
                    ATTR_FRIENDLY_NAME: "Aktualizacja",
                    "icon": "mdi:update",
                    "reinstall_dom_app": True,
                    "reinstall_android_app": android,
                    "apt": apt,
                    "beta": beta,
                },
            )

            hass.states.async_set(
                "script.ais_update_system",
                "off",
                {
                    ATTR_FRIENDLY_NAME: " Zainstaluj aktualizację",
                    "icon": "mdi:download",
                },
            )

            # notify about update
            hass.components.persistent_notification.async_create(
                title="Dostępna jest nowa wersja " + newest,
                message=(
                    info_for_screen + "[ Przejdz by zainstalować](/config/ais_dom)"
                ),
                notification_id="ais_update_notification",
            )

            # say info about update
            import homeassistant.components.ais_ai_service as ais_ai

            if say_it or (
                ais_ai.CURR_ENTITIE == "script.ais_update_system"
                and ais_ai.CURR_BUTTON_CODE == 23
            ):
                await hass.services.async_call(
                    "ais_ai_service", "say_it", {"text": info}
                )
            else:
                if ais_global.G_AIS_START_IS_DONE:
                    await hass.services.async_call(
                        "ais_ai_service", "say_it", {"text": info_for_screen}
                    )
        else:
            # dismiss update notification
            hass.components.persistent_notification.async_dismiss(
                "ais_update_notification"
            )
            info = "Twój system jest aktualny, wersja " + newest + ". "
            # only if not executed by scheduler
            import homeassistant.components.ais_ai_service as ais_ai

            if say_it or (
                ais_ai.CURR_ENTITIE == "script.ais_update_system"
                and ais_ai.CURR_BUTTON_CODE == 23
            ):
                if ais_global.G_AIS_START_IS_DONE:
                    await hass.services.async_call(
                        "ais_ai_service", "say_it", {"text": info}
                    )
            info += releasenotes
            hass.states.async_set(
                ENTITY_ID,
                info,
                {
                    ATTR_FRIENDLY_NAME: "Wersja",
                    "icon": "mdi:update",
                    "reinstall_dom_app": False,
                    "reinstall_android_app": False,
                    "apt": apt,
                    "beta": beta,
                },
            )
            hass.states.async_set(
                "script.ais_update_system",
                "off",
                {
                    ATTR_FRIENDLY_NAME: " Sprawdź dostępność aktualizacji",
                    "icon": "mdi:refresh",
                },
            )
            _LOGGER.info(
                "You are on the latest version (%s) of Assystent domowy", newest
            )

    # Update daily, start 1 hour after startup

    _dt = dt_util.utcnow() + timedelta(hours=1)
    event.async_track_utc_time_change(
        hass, check_new_version, hour=_dt.hour, minute=_dt.minute, second=_dt.second
    )

    # register services
    hass.services.async_register(DOMAIN, SERVICE_CHECK_VERSION, check_new_version)

    return True


async def get_system_info(hass, include_components):
    """Return info about the system."""

    gate_id = hass.states.get("sensor.ais_secure_android_id_dom").state
    info_object = {
        "arch": platform.machine(),
        "dev": "dev" in current_version,
        "docker": False,
        "os_name": platform.system(),
        "python_version": platform.python_version(),
        "timezone": dt_util.DEFAULT_TIME_ZONE.zone,
        "version": current_version,
        "virtualenv": os.environ.get("VIRTUAL_ENV") is not None,
        "hassio": hass.components.hassio.is_hassio(),
        "gate_id": gate_id,
    }

    if include_components:
        info_object["components"] = list(hass.config.components)

    if platform.system() == "Windows":
        info_object["os_version"] = platform.win32_ver()[0]
    elif platform.system() == "Darwin":
        info_object["os_version"] = platform.mac_ver()[0]
    elif platform.system() == "FreeBSD":
        info_object["os_version"] = platform.release()
    elif platform.system() == "Linux":
        import distro

        linux_dist = await hass.async_add_job(distro.linux_distribution, False)
        info_object["distribution"] = linux_dist[0]
        info_object["os_version"] = linux_dist[1]
        info_object["docker"] = os.path.isfile("/.dockerenv")

    return info_object


async def get_newest_version(hass, huuid, include_components):
    """Get the newest Ais dom version."""
    hass.states.async_set(
        ENTITY_ID,
        "sprawdzam",
        {
            ATTR_FRIENDLY_NAME: "Wersja",
            "icon": "mdi:update",
            "reinstall_dom_app": False,
            "reinstall_android_app": False,
        },
    )
    if huuid:
        info_object = await get_system_info(hass, include_components)
        info_object["huuid"] = huuid
    else:
        info_object = {}

    session = async_get_clientsession(hass)
    try:
        with async_timeout.timeout(10, loop=hass.loop):
            req = await session.post(UPDATER_URL, json=info_object)
        _LOGGER.info(
            (
                "Submitted analytics to AIS dom servers. "
                "Information submitted includes %s"
            ),
            info_object,
        )
    except (asyncio.TimeoutError, aiohttp.ClientError):
        _LOGGER.error("Could not contact AIS dom to check " "for updates")
        info = "Nie można skontaktować się z usługą AIS dom."
        info += "Spróbuj ponownie później."
        hass.states.async_set(
            ENTITY_ID,
            info,
            {
                ATTR_FRIENDLY_NAME: "Wersja",
                "icon": "mdi:update",
                "reinstall_dom_app": False,
                "reinstall_android_app": False,
            },
        )
        return None

    try:
        res = await req.json()
    except ValueError:
        _LOGGER.error("Received invalid JSON from AIS dom Update")
        info = "Wersja. Otrzmyano nieprawidłową odpowiedz z usługi AIS dom "
        hass.states.async_set(
            ENTITY_ID,
            info,
            {
                ATTR_FRIENDLY_NAME: "Wersja",
                "icon": "mdi:update",
                "reinstall_dom_app": False,
                "reinstall_android_app": False,
            },
        )
        return None

    try:
        res = RESPONSE_SCHEMA(res)
        if "apt" in res:
            return (
                res["version"],
                res["release-notes"],
                res["reinstall-android"],
                res["apt"],
            )
        else:
            return res["version"], res["release-notes"], res["reinstall-android"], ""
    except vol.Invalid:
        _LOGGER.error("Got unexpected response: %s", res)
        info = "Wersja. Otrzmyano nieprawidłową odpowiedz z usługi AIS dom "
        info += str(res)
        hass.states.async_set(
            ENTITY_ID,
            info,
            {
                ATTR_FRIENDLY_NAME: "Wersja",
                "icon": "mdi:update",
                "reinstall_dom_app": False,
                "reinstall_android_app": False,
            },
        )
        return None
