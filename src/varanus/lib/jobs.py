"""Actual job retrieval
"""
from typing import Generator
import varanus.models

JOB_FIELDS = (
    'project', 'spider', 'spider_args', 'job_cmd', 'tags', 'scrapystats', 'units',
    'version', 'priority', 'pending_time', 'running_time', 'finished_time', 'scheduled_by',
    'state', 'close_reason',
)


def Jobs(session,
         spider: str = None,
         suffix: str = None,
         count: int = None,
         running: bool = None,
         all_tags: list = None,
         **kwargs) -> Generator[dict, None, None]:
    """
    ``session``::

        <class 'varanus.session.Session'>
          ◇ client        <scrapinghub.client.ScrapinghubClient>
          ◇ config        <shub.config.ShubConfig>
          ◇ _session      <requests.sessions.Session>

    ``spider`` (str) The spider name::

          "amazon.us"

    ``suffix`` (str) The spider name suffix::

          ".co.uk"

    ``count`` (int) The number of jobs to request (1000 max)::

          10

    ``running`` (bool) Should we include running jobs?::

          False

    ``all_tags`` (list) Select only jobs that have all the given tags::

          ['consumed', 'to_be_delivered']

    ``kwargs`` (dict) Remaining arguments::

          {fields="version,priority",
           has_tag=["to_be_delivered"],
           lacks_tag=["delivered"]}

    Returns: a job objects generator of all the jobs that match the
    given criteria sorted decreasing by job key if for a single spider
    or else by timestamp::

        <class 'varanus.models.Job'>
          ◇ data          <scrapinghub.client.jobs.Job>
          ◇ key           '299923/10/1'
          ◇ project       <scrapinghub.client.projects.Project>

    .. note:: Supply the ``fields`` argument as a list of strings for
        just the fields you want

    .. todo:: Don't pass cliff args to scrapinghub iter
    """
    def jobs():
        """First pre-filter jobs remotely with the Shub API via
        ``kwargs``, e.g.::

            {fields="version,priority",
             has_tag=["to_be_delivered"],
             lacks_tag=["delivered"]}

        Then post filter jobs locally.

        .. tip:: Pre-filtering is more efficient.
        """
        # Pre-filter
        jobs = session.project.jobs.iter(meta=fields, **kwargs)
        # Post-filter
        if suffix:
            jobs = filter(name, jobs)
        if worker_arg:
            jobs = filter(args, jobs)
        if all_tags:
            jobs = filter(tags, jobs)
        return jobs

    def name(job):
        return job['spider'].endswith(suffix)

    def args(job):
        spider_args = ' '.join(job.get('spider_args', {}).keys())
        job_cmd = ' '.join(job.get('job_cmd', [None])[1:])
        return worker_arg in job_cmd or worker_arg in spider_args

    def tags(job):
        return all(tag in job.get('tags', ()) for tag in all_tags)

    def _sort(job):
        if spider:
            return int(job['key'].rpartition('/')[2])
        else:
            return job['ts']

    kwargs.update(
        spider=spider,
        state=('finished', 'running' if running else None),
        count=count,
    )
    worker_arg = kwargs.pop('worker_arg', None)
    fields = kwargs.pop('fields', JOB_FIELDS)

    for job in sorted(jobs(), key=_sort, reverse=True):
        yield varanus.models.Job(session.project, defaults=job)
