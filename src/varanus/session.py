"""Session management
"""
import scrapinghub
import shub.config
import varanus.network


class _Config():
    """Session configuration data

    .. todo:: Should be able to get rid of `shub` dep if we do it
        manually here as so far it is the only import of it
    """

    def __init__(self):
        config = shub.config.load_shub_config()
        self.apikeys = config.apikeys
        self.normalized_projects = config.normalized_projects
        self.default_project = config.normalized_projects.get('default', {}).get('id')


class Session():
    """Session data like client & session

    Modules in the core will add other things as well, e.g.:

    * Project will attach ``project``.
    * Spiders will attach ``spiders``.
    """

    def __init__(self):
        self.config = _Config()
        apikey = self.config.apikeys.get('default')
        self.client = scrapinghub.ScrapinghubClient(apikey, use_msgpack=False)
        self._session = self.client._connection._session

    def get_workers(self, paths, archived, count):
        yield from varanus.network.get_workers(self, paths, archived, count)
