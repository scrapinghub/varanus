"""
+-------------+--------------------------------------------------------+
| Field       | Value                                                  |
+-------------+--------------------------------------------------------+
| Activity    | <scrapinghub.client.activity.Activity>                 |
| Collections | <scrapinghub.client.collections.Collections>           |
| Frontiers   | <scrapinghub.client.frontiers.Frontiers>               |
| Jobs        | <scrapinghub.client.jobs.Jobs>                         |
| Key         | 299923                                                 |
| Settings    | <scrapinghub.client.projects.Settings>                 |
| Spiders     | <scrapinghub.client.spiders.Spiders>                   |
+-------------+--------------------------------------------------------+
"""
import logging
import cliff.show
import varanus.lib


class Project(cliff.show.ShowOne):
    """Show project attributes
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--project', '-p', type=int)
        parser.add_argument('--samples', dest='psamples', help='How many samples to retrieve for project', default=0)  # noqa
        status = parser.add_mutually_exclusive_group(required=False)
        status_help = 'Retrieve current project status information'
        status.add_argument('--status', dest='status', action='store_true', help=status_help)
        status.add_argument('--no-status', dest='status', action='store_false')
        parser.set_defaults(status=False)
        return parser

    def take_action(self, parsed_args):
        session = self.app.varanus_session
        kwargs = dict(parsed_args._get_kwargs())
        project = varanus.lib.Project(session, **kwargs)
        return show_project(project)


def show_project(project):
    """
    ``project``::

        <class 'scrapinghub.client.projects.Project'>
          ◇ _client       <scrapinghub.client.ScrapinghubClient>
          ◇ activity      <scrapinghub.client.activity.Activity>
          ◇ collections   <scrapinghub.client.collections.Collections>
          ◇ frontiers     <scrapinghub.client.frontiers.Frontiers>
          ◇ jobs          <scrapinghub.client.jobs.Jobs>
          ◇ key           '299923'
          ◇ settings      <scrapinghub.client.projects.Settings>
          ◇ spiders       <scrapinghub.client.spiders.Spiders>
    """
    head = (
        'Activity',
        'Collections',
        'Frontiers',
        'Jobs',
        'Key',
        'Samples',
        'Settings',
        'Spiders',
        'Status',
    )
    body = (
        project.activity,
        project.collections,
        project.frontiers,
        project.jobs,
        project.key,
        tuple(getattr(project, 'samples', ())),
        project.settings,
        project.spiders,
        getattr(project, 'status', None),
    )
    return (head, body)
