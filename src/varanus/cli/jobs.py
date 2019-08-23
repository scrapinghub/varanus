"""
+-------------+------------------------+------------------+-----+------+
| Key         | Spider                 | Finish           | Err | Warn |
+-------------+------------------------+------------------+-----+------+
| 299923/10/2 | centertheatregroup.org | 2019/05/21 14:10 |   0 |  180 |
| 299923/10/1 | centertheatregroup.org | 2019/05/20 18:47 |   0 |  179 |
+-------------+------------------------+------------------+-----+------+
"""
import logging
import cliff.lister
import varanus.lib


class Jobs(cliff.lister.Lister):
    """List jobs filtered by various options
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        _content_kwa = dict(
            nargs='?',
            default='results',
            choices=(
                'all',
                'args',
                'codes',
                'info',
                'results',
                # 'settings',
                'tags',
                'time',
            ),
        )
        parser = super().get_parser(prog_name)
        parser.add_argument('content', help='Job listing content', **_content_kwa)
        parser.add_argument('--project', '-p', type=int)
        parser.add_argument('--spider', '-s', help='Filter for given spider name')
        parser.add_argument('--key', '-k', dest='jobkey', action='append', help='Job key, e.g. 123/456/789 or just 456/789')  # noqa
        parser.add_argument('--all-tags', '-t', nargs='+', help='Jobs have all of the tags')
        parser.add_argument('--any-tags', dest='has_tag', nargs='+', help='Jobs have any of the tags')  # noqa
        parser.add_argument('--not-tags', dest='lacks_tag', nargs='+', help='Jobs do not have any of the tags ')  # noqa
        parser.add_argument('--arg', '-a', dest='worker_arg', help='Filter for given argument')
        parser.add_argument('--count', type=int, default=10, help='How many jobs show')
        parser.add_argument('--start', type=int, default=0, help='How many jobs to skip')
        parser.add_argument('--running', action='store_true', help='Also show running jobs')
        return parser

    def take_action(self, parsed_args):
        session = self.app.varanus_session
        kwargs = dict(parsed_args._get_kwargs())
        jobs = varanus.lib.Jobs(session, **kwargs)
        return jobs_matrix(jobs, parsed_args.columns, parsed_args.content)


def jobs_matrix(jobs, columns: list, content: str):
    """Call appropriate content device on each Job

    ``jobs``::

        ( <varanus.models.Job object>, <varanus.models.Job object> )

    ```columns```::

        ["Spider", "RPM"]

    ``content``::

        "results"

    ``data``::

        ((('Key   ', '299923/10/2'),
          ('Spider', 'centertheatregroup.org'),
          ('Start ', '2019/05/21 13:55'),
          ('Finish', '2019/05/21 14:10'),
          ('Reason', 'finished')),
         (('Key   ', '299923/10/1'),
          ('Spider', 'centertheatregroup.org'),
          ('Start ', '2019/05/20 18:37'),
          ('Finish', '2019/05/20 18:47'),
          ('Reason', 'finished')))

    ``head``::

        ( 'Key', 'Spider', 'Start', 'Finish', 'Reason' )

    ``body``::

        (('299923/10/2',
          'centertheatregroup.org',
          '2019/05/21 13:55',
          '2019/05/21 14:10',
          'finished'),
         ('299923/10/1',
          'centertheatregroup.org',
          '2019/05/20 18:37',
          '2019/05/20 18:47',
          'finished'))
    """
    cols = columns or _Columns[content]
    data = tuple(_Job(job).data_by_columns(cols) for job in jobs)
    head = tuple(col[0] for col in (data[0] if data else ()))
    body = tuple(tuple(col[1] for col in row) for row in data)
    return (head, body)


_Columns = dict(
    all=(
        '200s',
        '300s',
        '400s',
        '500s',
        'Age days',
        'Arguments',
        'Err',
        'Finish',
        'GET/POST',
        'IPM',
        'Items',
        'Key',
        'Logs',
        'Pages',
        'Pnd mins',
        'Reason',
        'RPM',
        'Run mins',
        'Spider',
        'Start',
        'State',
        'Tags',
        'Units',
        'Version',
        'Warn',
    ),
    args=(
        'Key',
        'Spider',
        'Arguments',
    ),
    codes=(
        'Key',
        'Spider',
        'RPM',
        'IPM',
        'GET/POST',
        '200s',
        '300s',
        '400s',
        '500s',
    ),
    info=(
        'Key',
        'Spider',
        'Version',
        'Units',
        'Age days',
        'Pnd mins',
        'Run mins',
        'Start',
        'Finish',
        'Err',
        'Warn',
    ),
    results=(
        'Key',
        'Spider',
        'Pnd mins',
        'Run mins',
        'Start',
        'Finish',
        'Err',
        'Warn',
        'Items',
        'Pages',
        'State',
        'Reason',
        'Version',
    ),
    tags=(
        'Key',
        'Spider',
        'Tags',
    ),
    time=(
        'Key',
        'Spider',
        'Age days',
        'Pnd mins',
        'Run mins',
        'Start',
        'Finish',
        'RPM',
        'IPM',
    ),
)


class _Job():
    """Apply the content presentation logic"""

    def __init__(self, job):
        """
        ``job``::

            <varanus.models.Job object>
        """
        self.job = job
        self.stats = job.scrapystats
        self.get = self.stats.get('crawlera/request/method/GET', 0)  # TODO maybe not Crawlera?
        self.post = self.stats.get('crawlera/request/method/POST', 0)  # TODO maybe not Crawlera?
        self.mins = job.running_mins

    def _stat(self, prefix: str):
        """
        ``prefix``::

            'downloader/response_status_count/200'

        ``stats``::

            ['downloader/response_status_count/200']
        """
        stats = filter(lambda s: s.startswith(prefix), self.stats)
        return sum(self.stats[stat] for stat in stats)

    def data_by_columns(self, columns: list):
        all_columns_data = {
            '200s': self._stat('downloader/response_status_count/2'),
            '300s': self._stat('downloader/response_status_count/3'),
            '400s': self._stat('downloader/response_status_count/4'),
            '500s': self._stat('downloader/response_status_count/5'),
            'Age days': self.job.age,
            'Arguments': self.job.spider_args,
            'Err': self._stat('log_count/ERROR'),
            'Finish': self.job.dt.finished,
            'GET/POST': round(self.get / self.post * 100) if self.post else self.get,
            'IPM': self.job.items_per_min,
            'Items': self.job.items,
            'Key': self.job.key,
            'Logs': self.job.logs,
            'Pages': self.job.pages,
            'Pnd mins': self.job.pending_mins,
            'Reason': self.job.close_reason,
            'RPM': self.job.pages_per_min,
            'Run mins': self.job.running_mins,
            'Spider': self.job.spider,
            'Start': self.job.dt.running,
            'State': self.job.state,
            'Tags': self.job.tags,
            'Units': self.job.units,
            'Version': self.job.version,
            'Warn': self._stat('log_count/WARNING'),
        }
        return tuple((c, all_columns_data.get(c)) for c in columns)
