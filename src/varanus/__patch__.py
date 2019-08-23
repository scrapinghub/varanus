""" Monkey patches

These patches replace the ``scrapinghub`` network requests routines with
identical versions with the addition of logging the responses.

.. important:: Each new version of ``scrapinghub`` will need to be
    checked to make sure these routines have not been updated; and,
    if so then those changes will also need to be reflected here.

.. todo:: Inject code instead of replacing routines.
"""
import logging
import requests
import scrapinghub.legacy
import scrapinghub.client
import scrapinghub.client.exceptions

from .network import log_response

hsc_logger = logging.getLogger('HubstorageClient')

__patches__ = {
    'scrapinghub.client.HubstorageClient.request': 'python-scrapinghub/2.1.1',
    'scrapinghub.legacy.Connection._request': 'python-scrapinghub/2.1.1',
}


def HubstorageClient_request(self, is_idempotent=False, **kwargs):
    """Execute an HTTP request with the current client session

    Use the retry policy configured in the client when is_idempotent is True.
    """
    kwargs.setdefault('timeout', self.connection_timeout)

    def invoke_request():
        r = self.session.request(**kwargs)
        log_response(
            r,
            source=f'{__name__}:scrapinghub.client.HubstorageClient.request',
            color='blue',
        )
        try:
            r.raise_for_status()
            return r
        except requests.HTTPError as e:
            hsc_logger.debug('%s: %s', r, r.content)
            raise scrapinghub.client.exceptions.NotFound(http_error=e)

    if is_idempotent:
        return self.retrier.call(invoke_request)
    else:
        return invoke_request()


def Connection_request(self, url, data, headers, format, raw, files=None):
    """Performs the request using and returns the content deserialized,
    based on given `format`

    Available formats:
        * json - Returns a json object and checks for errors
        * jl   - Returns a generator of json object per item

    Raises APIError if json response have error status.
    """
    if format not in ('json', 'jl') and not raw:
        raise scrapinghub.legacy.APIError(
            "format must be either json or jl",
            _type=scrapinghub.legacy.APIError.ERR_VALUE_ERROR)

    if data is None and files is None:
        response = self._session.get(url, headers=headers,
                                     timeout=self._connection_timeout)
    else:
        response = self._session.post(url, headers=headers,
                                      data=data, files=files,
                                      timeout=self._connection_timeout)
    log_response(
        response,
        source=f'{__name__}:scrapinghub.legacy.Connection._request',
        color='cyan',
    )
    return self._decode_response(response, format, raw)


scrapinghub.client.HubstorageClient.request = HubstorageClient_request
scrapinghub.legacy.Connection._request = Connection_request
