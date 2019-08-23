import logging
import cliff.lister
import varanus.lib


class Stats(cliff.lister.Lister):
    """Show jobs statistics
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('stats', nargs='*', help='Statistics to analyze')
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
        return jobs_matrix(jobs, parsed_args.stats)


def jobs_matrix(jobs, terms):
    """Return job stats ready to be formatted
    """
    # List of all stats keys for all jobs
    stats = set()
    jobs = tuple(jobs)
    for job in jobs:
        stats.update(
            stat for stat in job.scrapystats
            if not terms or any(term in stat for term in terms))
    stats = sorted(stats)

    def headers():
        yield from ('Job Key', 'Worker')
        yield from stats

    def fields(j):
        yield from (j.key, j.spider)
        for stat in stats:
            yield j.scrapystats.get(stat, '')

    head = tuple(headers())
    body = tuple(tuple(fields(job)) for job in jobs)
    return (head, body)
