"""Actual worker retrieval
"""
import varanus.models


def Workers(session,
            paths: list = [],
            count: int = 0,
            load: bool = False,
            recent: bool = False,
            archived: bool = None,
            **kwargs):
    """
    ``session``::

        <class 'varanus.session.Session'>
          ◇ client        <scrapinghub.client.ScrapinghubClient>
          ◇ config        <shub.config.ShubConfig>
          ◇ project       <scrapinghub.client.projects.Project>
          ◇ _session      <requests.sessions.Session>

    Returns: a Worker objects generator

    ,, todo:: Pagination!
    """
    spider_map = {}
    if recent:
        hs_client = session.client._hsclient
        project = hs_client.get_project(session.project.key)
        summary = project.spiders.lastjobsummary(count=1000)
        spider_map = {job['spider']: job for job in summary}

    for worker in session.get_workers(paths, archived, count):
        if load and not worker.get('jobq_id'):
            worker['jobq_id'] = session.project.spiders.get(worker['name'])._id
        worker = varanus.models.Worker(session.project, worker)
        job = spider_map.get(worker.name)
        if job:
            worker.jobs.append(job)
        yield worker
