"""HTTP connector class to Bosch thermostat."""
import logging
from aiohttp import client_exceptions

from .const import HTTP_HEADER
from .errors import RequestError, Response404Error, ResponseError

_LOGGER = logging.getLogger(__name__)


class HttpConnector:
    """HTTP connector to Bosch thermostat."""

    def __init__(self, host, websession):
        """Init of HTTP connector."""
        self._host = host
        self._websession = websession
        self._request_timeout = 10

    async def request(self, path):
        """Make a get request to the API."""
        _LOGGER.debug("Sending request to %s", path)
        try:
            async with self._websession.get(
                    self._format_url(path),
                    headers=HTTP_HEADER,
                    timeout=self._request_timeout,
                    skip_auto_headers=['Accept-Encoding', 'Accept']) as res:
                if res.status == 200:
                    if res.content_type != 'application/json':
                        raise ResponseError('Invalid content type: {}'.
                                            format(res.content_type))
                    else:
                        data = await res.text()
                        return data
                elif res.status == 404:
                    raise Response404Error('URI not exists: {}'.
                                           format(path))
                else:
                    raise ResponseError('Invalid response code: {}'.
                                        format(res.status))
        except (client_exceptions.ClientError,
                client_exceptions.ClientConnectorError,
                TimeoutError) as err:
            raise RequestError(
                'Error requesting data from {}: {}'.format(path, err)
            ) from err

    async def submit(self, path, data):
        """Make a put request to the API."""
        try:
            _LOGGER.debug("Sending request to %s", path)
            async with self._websession.put(
                    self._format_url(path),
                    data=data,
                    headers=HTTP_HEADER,
                    timeout=self._request_timeout) as req:
                data = await req.text()
                _LOGGER.debug("Send request returned status %s with data %s",
                              req.status, data)
                return data
        except (client_exceptions.ClientError, TimeoutError) as err:
            raise RequestError(
                'Error putting data to {}, path: {}, message: {}'.
                format(self._host, path, err)
            )

    def _format_url(self, path):
        """Format URL to make requests to gateway."""
        return 'http://{}{}'.format(self._host, path)

    def set_timeout(self, timeout=10):
        """Set timeout for API calls."""
        self._request_timeout = timeout
