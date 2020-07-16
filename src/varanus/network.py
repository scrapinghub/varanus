""" Varanus network calls
"""
import urllib.parse
from typing import Any


def log_response(response, source=None, color=None):
    # TODO use Cliff logging
    import colorama
    if color == 'blue':
        fS = colorama.Back.BLUE + colorama.Fore.BLACK + colorama.Style.DIM
        cS = colorama.Fore.BLUE
    elif color == 'cyan':
        fS = colorama.Back.CYAN + colorama.Fore.BLACK + colorama.Style.DIM
        cS = colorama.Fore.CYAN
    else:
        fS = colorama.Back.MAGENTA + colorama.Fore.BLACK + colorama.Style.DIM
        cS = colorama.Fore.MAGENTA
    dS = colorama.Style.DIM
    xS = colorama.Style.RESET_ALL
    if source is None:
        from inspect import currentframe, getframeinfo
        f = getframeinfo(currentframe().f_back)
        source = f'{f.filename}::{f.function}:{f.lineno}'
    print(
        fS, '●▬▬▬▬▬▬▬▬▬●', xS,
        cS, response, response.url, '●',
        dS, source, xS,
    )


def RequestJson(session, url: str, method='GET', query: dict = {}, data: (dict, Any) = None):
    """
    Grab data using the session

    .. note:: Uses client session (requests)
    .. seealso:: http://docs.python-requests.org/en/master/api
    .. warning:: This function makes a blocking network request
    """
    query = dict(query)
    query.setdefault('format', 'json')
    response = session._session.request(url=url, method=method, params=query, json=data)
    if app.options.debug:
        log_response(response)
    if response.ok:
        return response.json() if response.content else ''
    else:
        raise LookupError(response.text)


def get_results(url: str, session):
    """Return results from given url
    .. seealso:: https://github.com/scrapinghub/hubstorage/tree/develop/servlet#id-lookup-api
    .. todo:: Pagination: handle `next` attribute (url)
    """
    return RequestJson(session, url)['results']


def get_workers(session, paths: tuple = (), archived: bool = None, count: int = 100):
    """Return workers
    """
    http = 'https://app.scrapinghub.com/api/v2'

    query = {}
    if archived is not None:
        query['archived'] = 1 if archived else 0
    if count is not None:
        query['page_size'] = int(count)
    qs = urllib.parse.urlencode(query)

    for path in paths:
        url = f'{http}/projects/{session.project.key}/{path}?{qs}'
        for result in get_results(url, session):
            yield result
