"""Actual collection retrieval
"""
import varanus.models


def CollectionItems(session,
                    filter: str = None,
                    count: int = 0,
                    name: str = None,
                    key: str = None,
                    **kwargs
                    ):
    """
    ``session``::

        <class 'varanus.session.Session'>
          ◇ client        <scrapinghub.client.ScrapinghubClient>
          ◇ config        <shub.config.ShubConfig>
          ◇ _session      <requests.sessions.Session>

    Returns: a generator of items from the named collection
    """
    store = session.project.collections.get_store(name)
    collection = varanus.models.Collection(store)

    if key:
        yield from collection.item(key)
    else:
        yield from collection.items(count, filter=filter)
