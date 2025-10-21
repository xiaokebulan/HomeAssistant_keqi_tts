"""Support for the Ke Qi speech service."""
from http import HTTPStatus
import logging
import asyncio
import aiohttp
import async_timeout
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider

_LOGGER = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = [
    'zh',
    'cte',
    'en',
    'ara',
    'de',
    'fra',
    'jp',
    'kor',
    'pt',
    'ru',
    'spa',
    'th',
]

CONF_SPEED = 'speed'
CONF_URL = 'url'

DEFAULT_LANG = 'zh'
DEFAULT_SPEED = 5
DEFAULT_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_URL): cv.string,
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): cv.string,
        vol.Optional(CONF_SPEED, default=DEFAULT_SPEED): int,
    }
)


async def async_get_engine(hass, config, discovery_info=None):
    """Set up the component."""
    return KeQiProvider(hass, config)


class KeQiProvider(Provider):
    """The provider."""

    def __init__(self, hass, config):
        """Init service."""
        self.name = 'Ke Qi TTS'
        self.hass = hass
        self._config = config or {}

    @property
    def default_language(self):
        """Return the default language."""
        return self._config.get(CONF_LANG)

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORTED_LANGUAGES

    async def async_get_tts_audio(self, message, language, options=None):
        """Load TTS audio."""
        options = options or {}
        session = async_get_clientsession(self.hass)
        data = None
        try:
            with async_timeout.timeout(15):
                params = {
                    'text': message
                }
                headers = {
                    'Referer': self._config.get(CONF_URL),
                    'User-Agent': DEFAULT_AGENT,
                }
                request = await session.get(
                    self._config.get(CONF_URL),
                    params=params
                )
                if request.status != HTTPStatus.OK:
                    _LOGGER.error(
                        'Got error %d on load URL %s', request.status, request.url
                    )
                data = await request.read()
        except (asyncio.TimeoutError, aiohttp.ClientError) as exc:
            _LOGGER.error('Got error from Ke Qi speech API %s', exc)
        if not data:
            return None, None
        return 'mp3', data
