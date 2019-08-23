"""Actual project retrieval
"""


def Project(session, project: int = None, psamples: int = 0, status: bool = False, **kwargs):
    """
    ``session``::

        <class 'varanus.session.Session'>
          ◇ client        <scrapinghub.client.ScrapinghubClient>
          ◇ config        <shub.config.ShubConfig>
          ◇ _session      <requests.sessions.Session>

    Returns: a Scrapinghub project object::

        <class 'scrapinghub.client.projects.Project'>
          ◇ _client       <scrapinghub.client.ScrapinghubClient>
          ◇ activity      <scrapinghub.client.activity.Activity>
          ◇ collections   <scrapinghub.client.collections.Collections>
          ◇ frontiers     <scrapinghub.client.frontiers.Frontiers>
          ◇ jobs          <scrapinghub.client.jobs.Jobs>
          ◇ key           '299923'
          ◇ settings      <scrapinghub.client.projects.Settings>
          ◇ spiders       <scrapinghub.client.spiders.Spiders>

    .. todo:: Why does status make two (2) requests instead of just one?

        https://storage.scrapinghub.com/projects/299923/jobsummary
        https://storage.scrapinghub.com/projects/299923/jobsummary
    """
    if project is None:
        project = getattr(session, 'project', session.config.default_project)

    if isinstance(project, (int, str)):
        project = session.client.get_project(project)

    if psamples or status:
        hs_project = session.client._hsclient.get_project(project.key)
        if psamples:
            project.samples = hs_project.samples.list(count=psamples)
        if status:
            project.status = hs_project.jobsummary()

    return project
