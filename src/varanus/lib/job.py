"""Actual job retrieval
"""
import varanus.models


def Job(session, jobkey: str = '', **kwargs):
    """
    ``session``::

        <class 'varanus.session.Session'>
          ◇ client        <scrapinghub.client.ScrapinghubClient>
          ◇ config        <shub.config.ShubConfig>
          ◇ _session      <requests.sessions.Session>

    ``jobkey`` (str) The job key in the format p/s/j::

        123/456/789

    Returns: a Job object::

        <class 'varanus.models.Job'>
          ◇ data          <scrapinghub.client.jobs.Job>
          ◇ key           '299923/10/1'
          ◇ project       <scrapinghub.client.projects.Project>
    """
    defaults = {}

    job = session.project.jobs.get(jobkey)

    if kwargs.get('jsamples'):
        defaults['samples'] = job.samples.list(count=kwargs['jsamples'])

    return varanus.models.Job(session.project, jobkey, defaults=defaults, data=job)
