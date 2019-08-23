"""Actual job retrieval
"""


def Item(session, itemkey: str = '', **kwargs):
    """
    ``session``::

        <class 'varanus.session.Session'>
          ◇ client        <scrapinghub.client.ScrapinghubClient>
          ◇ config        <shub.config.ShubConfig>
          ◇ _session      <requests.sessions.Session>

    ``itemkey`` (str) The item key in the format p/s/j/i::

        123/456/789/0

    Returns: dict
    """
    jk, _, item_index = itemkey.rpartition('/')
    job = session.project.jobs.get(jk)
    return job.items.get(item_index)
