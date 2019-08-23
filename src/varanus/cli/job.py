"""
+---------------+-----------------------------------------------------+
| Field         | Value                                               |
+---------------+-----------------------------------------------------+
| _shub_worker  | kumo                                                |
| age           | 0                                                   |
| api_url       | https://staging.scrapinghub.com/api/                |
| close_reason  | finished                                            |
| completed_by  | jobrunner                                           |
| data          | <scrapinghub.client.jobs.Job>                       |
| deploy_id     | 23                                                  |
| dt            | <varanus.models.Timed.dt.<locals>.DateTime>            |
| elapsed       | 0                                                   |
| finished_time | 1558378041601                                       |
| items         | 0                                                   |
| key           | 299923/10/1                                         |
| logs          | 0                                                   |
| metajob       | <varanus.models.MetaJob object at 0x7f63e3ac6278>      |
| pages         | 0                                                   |
| pending_mins  | 0                                                   |
| pending_time  | 1558377459114                                       |
| priority      | 2                                                   |
| project       | <scrapinghub.client.projects.Project>               |
| running_mins  | 10                                                  |
| running_secs  | 582.454                                             |
| running_time  | 1558377459147                                       |
| scheduled_by  | steven                                              |
| spider        | centertheatregroup.org                              |
| spider_args   | {}                                                  |
| spider_type   | manual                                              |
| started_by    | jobrunner                                           |
| state         | finished                                            |
| tags          | []                                                  |
| ts            | 0                                                   |
| units         | 1                                                   |
| version       | enhancement-1164-g765c7788-sma.www-pelican          |
+---------------+-----------------------------------------------------+
"""
import logging
import cliff.show
import varanus.lib


class Job(cliff.show.ShowOne):
    """List job attributes for a given job key
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('jobkey', help='The job key, e.g. 123/456/789 or just 456/789')
        parser.add_argument('--project', '-p', type=int)
        parser.add_argument('--samples', dest='jsamples', help='How many samples to retrieve for job', default=0)  # noqa
        return parser

    def take_action(self, parsed_args):
        session = self.app.varanus_session
        kwargs = dict(parsed_args._get_kwargs())
        return show_job(varanus.lib.Job(session, **kwargs))


def show_job(job):
    """
    ``job``::

        <class 'varanus.models.Job'>
          ◇ _shub_worker      'kumo'
          ◇ age               0
          ◇ api_url           'https://staging.scrapinghub.com/api/'
          ◇ close_reason      'finished'
          ◇ completed_by      'jobrunner'
          ◇ data              <scrapinghub.client.jobs.Job object at 0
          ◇ deploy_id         23
          ◇ dt                <varanus.models.Timed.dt.<locals>.DateTime
          ◇ elapsed           0
          ◇ finished_time     1558378041601
          ◇ items             0
          ◇ key               '299923/10/1'
          ◇ logs              0
          ◇ metadata          {'_shub_worker': 'kumo', 'api_url': 'htt
          ◇ metajob           <varanus.models.MetaJob object at 0x7facd93
          ◇ pages             0
          ◇ pending_mins      0
          ◇ pending_time      1558377459114
          ◇ priority          2
          ◇ project           <scrapinghub.client.projects.Project obj
          ◇ running_mins      10
          ◇ running_secs      582.454
          ◇ running_time      1558377459147
          ◇ scheduled_by      'steven'
          ◇ scrapystats       {'crawlera/request': 177, 'crawlera/requ
          ◇ spider            'centertheatregroup.org'
          ◇ spider_args       {}
          ◇ spider_type       'manual'
          ◇ started_by        'jobrunner'
          ◇ state             'finished'
          ◇ tags              []
          ◇ ts                0
          ◇ units             1
          ◇ version           'enhancement-1164-g765c7788-sma.www-peli
    """
    def fields():
        for field in dir(job):
            if not field.startswith('__') and field not in ('metadata', 'scrapystats'):
                yield field

    head = tuple(fields())
    body = tuple(getattr(job, field) for field in head)
    return (head, body)
