"""Scrapinghub scripts access
"""
from .workers import Workers as _Workers  # noqa


class Workers(_Workers):
    """Scripts logic

    .. warning:: TODO: Currently the ``jobq_id`` is zero because
    The results from the scripts Scrapinghub api call does not contain
    the jobsq id so you need to call LoadSpiderData to grab the data for
    each one individually.

    class Worker():
        def LoadSpiderData(self):
            script = self.project.spiders.get(self.name)
            self.jobq_id = script._id
            self._ = script
            self.key = script.key
    """
    paths = ('scripts',)
